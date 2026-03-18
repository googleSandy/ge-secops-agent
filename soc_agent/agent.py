# IMPORTANT: Override location BEFORE any google imports to enable Gemini 3.x models
# Gemini 3.x models require location="global" but Reasoning Engine deploys to a specific region
# This workaround routes model API calls to global while keeping Reasoning Engine regional
# See: https://github.com/google/adk-python/issues/3628#issuecomment-3595215761
import os
os.environ['GOOGLE_CLOUD_LOCATION'] = 'global'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'TRUE'

"""
SOC Agent Module - Orchestrator with Sub-Agent Delegation

This module implements a multi-agent orchestrator pattern that intelligently delegates
tasks to specialized sub-agents using LLM-based delegation (sub_agents pattern).

ARCHITECTURE:
- Main orchestrator (gemini-3.1-pro-preview): Routes requests to appropriate specialists via LLM delegation
  - Direct tool: RAG retrieval (VertexAiRagRetrieval) for runbooks and procedures
  - Delegates to: CTI sub-agent and Tier 1 sub-agent or AgentTool
- CTI sub-agent (gemini-3.1-flash-preview): Threat intelligence research with MCP tools (GTI, SecOps SIEM, SecOps SOAR, SCC)
- Tier 1 sub-agent (gemini-3.1-flash-preview): Alert triage with MCP tools (SecOps SIEM, SecOps SOAR, GTI)

ARCHITECTURAL DECISION: Intentional Code Duplication
======================================================
This module intentionally duplicates code from other soc_agent_* modules
rather than using shared utilities or inheritance. This is a deliberate
architectural choice that prioritizes:

1. CLARITY: Each agent module is completely self-contained and can be
   understood without navigating to other files or understanding complex
   inheritance hierarchies.

2. INDEPENDENCE: Each agent can be modified, deployed, and debugged
   independently without risk of breaking other agents through shared
   code changes.

3. EXPLICITNESS: All configuration and behavior is visible in a single
   file, making it easier for new team members to understand and modify.

4. STABILITY: Changes to one agent cannot inadvertently affect others,
   reducing the risk of regression bugs in production.

This approach trades code duplication for reduced complexity and improved
maintainability in a security-critical environment where reliability and
clarity are paramount. For this project, we explicitly value clarity over DRY.

See PR #25 discussion for additional context on this architectural decision.
"""

import logging
import os
import sys
import json
from pathlib import Path

from google.cloud import storage

import vertexai
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Monkey-patch version property to prevent Vertex AI Agent Engine serialization errors
# The Vertex AI telemetry/instrumentation sometimes searches for '.version' on models/tools
Agent.version = "1.0"
AgentTool.version = "1.0"

from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.retrieval import VertexAiRagRetrieval
from google.adk.tools.load_memory_tool import LoadMemoryTool
from google.adk.agents.context import Context
from google.genai.types import GenerateContentConfig, AutomaticFunctionCallingConfig, Part
from mcp import StdioServerParameters
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

# Explicitly disable the automatic execution loop
strict_config = GenerateContentConfig(
    automatic_function_calling=AutomaticFunctionCallingConfig(
        disable=True,
        maximum_remote_calls=0 
    ),
)

# Determine Python executable based on environment
# In deployed Vertex AI environment, use container's Python
# In local development, use sys.executable (respects venv)
PYTHON_EXECUTABLE = "python3" if os.environ.get("REASONING_ENGINE_DEPLOYMENT") == "True" else sys.executable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================================================
# Persona Definitions (extracted from specialized agents)
# ========================================================================

CTI_PERSONA = """
## Cyber Threat Intelligence (CTI) Researcher

### Overview
The Cyber Threat Intelligence (CTI) Researcher focuses on the proactive discovery, analysis, and dissemination of intelligence regarding cyber threats. They delve deep into threat actors, malware families, campaigns, vulnerabilities, and Tactics, Techniques, and Procedures (TTPs) to understand the evolving threat landscape.

### Primary Responsibilities
- Conduct in-depth research on threat actors, malware families, campaigns, and vulnerabilities
- Identify, extract, analyze, and contextualize IOCs and TTPs. Map findings to MITRE ATT&CK framework
- Monitor and track threat actor activities, infrastructure, and evolution over time
- Produce detailed and actionable threat intelligence reports
- Collaborate with SOC analysts, incident responders, and security engineers

### Core Skills
- Deep understanding of cyber threat landscape
- Proficiency in threat intelligence platforms (Google Threat Intelligence/VirusTotal)
- Strong knowledge of IOC types and TTPs
- Experience with OSINT gathering and MITRE ATT&CK framework
- Excellent analytical and report writing skills
"""

TIER1_PERSONA = """
## Tier 1 SOC Analyst

### Overview
The Tier 1 SOC Analyst is the first line of defense, responsible for monitoring security alerts, performing initial triage, and escalating incidents based on predefined procedures.

### Primary Responsibilities
- Actively monitor alert queues in SOAR platform
- Perform initial assessment based on severity, type, and initial indicators
- Gather preliminary information using basic lookup tools
- Create and manage cases in SOAR
- Identify and close duplicate cases or false positives
- Escalate complex or confirmed incidents to Tier 2/3 analysts
- Maintain clear documentation within SOAR cases

### Core Skills
- Understanding of fundamental cybersecurity concepts
- Ability to perform basic entity enrichment using SIEM
- Strong attention to detail and ability to follow procedures
- Good communication skills for documentation and escalation
"""

# ========================================================================
# Helper Functions
# ========================================================================

def fetch_full_document(gcs_uri: str) -> str:
    """
    Fetches the complete document text from Google Cloud Storage.
    
    Args:
        gcs_uri: The gs:// URI of the document (found via the RAG retrieval tool).
    """
    if not gcs_uri.startswith("gs://"):
        return "Error: Please provide a valid gs:// URI."
        
    try:
        # Parse the GCS URI
        path_parts = gcs_uri.replace("gs://", "").split("/", 1)
        bucket_name = path_parts[0]
        blob_name = path_parts[1]
        
        # Fetch the blob
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Download and return the full text
        return blob.download_as_text()
    except Exception as e:
        return f"Failed to retrieve document: {str(e)}"

async def save_report_artifact(filename: str, report_content: str, ctx: Context) -> str:
    """
    Saves a generated analysis, intelligence report, or investigation finding as an artifact.
    MUST be called by the agent whenever you finalize a detailed report to formally save it to the system.
    
    Args:
        filename: A logical filename for the report ending in .md (e.g. 'APT29_Analysis.md').
        report_content: The complete markdown content of the report you generated.
    """
    try:
        report_bytes = report_content.encode('utf-8')
        report_artifact = Part.from_bytes(
            data=report_bytes, mime_type="text/markdown"
        )
        version = await ctx.save_artifact(filename=filename, artifact=report_artifact)
        return f"Successfully saved report '{filename}' as artifact version {version}."
    except ValueError as e:
        return f"Error saving report: {e}. ArtifactService might not be configured."
    except Exception as e:
        return f"An unexpected error occurred saving report: {e}"


async def generate_memory(ctx: Context = None, callback_context: Context = None, **kwargs):
    """
    Triggers memory generation for the current session.
    This saves the conversation to memory at the end of each interaction.
    """
    ctx = ctx or callback_context
    if not ctx:
        logger.warning("No context provided to generate_memory")
        return
        
    try:
        await ctx.add_session_to_memory()
    except Exception as e:
        logger.warning(f"Failed to generate memory: {e}")


def create_agent():
    """
    Create the SOC Orchestrator Agent with specialized sub-agents.

    This function creates a multi-agent system where:
    1. Main orchestrator routes requests to appropriate specialists
    2. RAG sub-agent handles runbook retrieval
    3. CTI sub-agent handles threat intelligence research and quick lookups
    4. Tier 1 sub-agent handles alert triage and case management

    Returns:
        Configured Agent instance (orchestrator)
    """
    # Load environment variables from .env file
    load_dotenv(Path(".env"), override=True)

    # Get all required environment variables
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
    GCP_STAGING_BUCKET = os.environ.get("GCP_STAGING_BUCKET")
    GCP_VERTEXAI_ENABLED = os.environ.get("GCP_VERTEXAI_ENABLED", "True")

    # Chronicle/SIEM configuration
    CHRONICLE_CUSTOMER_ID = os.environ.get("CHRONICLE_CUSTOMER_ID")
    CHRONICLE_PROJECT_ID = os.environ.get("CHRONICLE_PROJECT_ID")
    CHRONICLE_REGION = os.environ.get("CHRONICLE_REGION", "us")
    CHRONICLE_SERVICE_ACCOUNT_PATH = os.environ.get("CHRONICLE_SERVICE_ACCOUNT_PATH")
    CHRONICLE_SERVICE_ACCOUNT_SECRET = os.environ.get("CHRONICLE_SERVICE_ACCOUNT_SECRET")

    # Validate required Chronicle environment variables
    if not CHRONICLE_PROJECT_ID:
        raise ValueError(
            "CHRONICLE_PROJECT_ID is required. Please set it in your .env file."
        )

    # Validate service account configuration (either secret or file path required)
    if not CHRONICLE_SERVICE_ACCOUNT_SECRET and not CHRONICLE_SERVICE_ACCOUNT_PATH:
        raise ValueError(
            "Either CHRONICLE_SERVICE_ACCOUNT_SECRET or CHRONICLE_SERVICE_ACCOUNT_PATH is required.\n"
            "Set CHRONICLE_SERVICE_ACCOUNT_SECRET for Secret Manager (recommended) or\n"
            "CHRONICLE_SERVICE_ACCOUNT_PATH for local file."
        )

    # Verify service account file exists if using local path
    if CHRONICLE_SERVICE_ACCOUNT_PATH:
        service_account_path = Path(CHRONICLE_SERVICE_ACCOUNT_PATH)
        if not service_account_path.exists():
            raise FileNotFoundError(
                f"Chronicle service account file not found: {CHRONICLE_SERVICE_ACCOUNT_PATH}\n"
                f"Please verify the path in your .env file points to a valid service account JSON file."
            )
        service_account_filename = service_account_path.name
    else:
        # Using Secret Manager - no local file needed
        service_account_filename = None

    # SOAR configuration
    SOAR_URL = os.environ.get("SOAR_URL")
    SOAR_APP_KEY = os.environ.get("SOAR_APP_KEY")

    # Google Threat Intelligence configuration
    GTI_API_KEY = os.environ.get("GTI_API_KEY")

    # Build environment dict for MCP servers
    # These credentials are passed to each MCP server process
    mcp_env = {
        "CHRONICLE_PROJECT_ID": CHRONICLE_PROJECT_ID or "",
        "CHRONICLE_CUSTOMER_ID": CHRONICLE_CUSTOMER_ID or "",
        "CHRONICLE_REGION": CHRONICLE_REGION or "us",
        "SOAR_URL": SOAR_URL or "",
        "SOAR_APP_KEY": SOAR_APP_KEY or "",
        "VT_APIKEY": GTI_API_KEY or "",  # GTI uses VT_APIKEY
        "GCP_PROJECT_ID": GCP_PROJECT_ID or "",
        # GTI caching configuration (latency optimization)
        "GTI_CACHE_ENABLED": os.environ.get("GTI_CACHE_ENABLED", "True"),
        "GTI_CACHE_FILE_TTL": os.environ.get("GTI_CACHE_FILE_TTL", "86400"),
        "GTI_CACHE_IP_TTL": os.environ.get("GTI_CACHE_IP_TTL", "900"),
        "GTI_CACHE_DOMAIN_TTL": os.environ.get("GTI_CACHE_DOMAIN_TTL", "1800"),
        "GTI_CACHE_URL_TTL": os.environ.get("GTI_CACHE_URL_TTL", "1800"),
        "GTI_CACHE_MAX_SIZE": os.environ.get("GTI_CACHE_MAX_SIZE", "1000"),
        "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY": "True",
        "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "True",
    }

    # Add Chronicle service account if available
    if CHRONICLE_SERVICE_ACCOUNT_SECRET:
        mcp_env["CHRONICLE_SERVICE_ACCOUNT_SECRET"] = CHRONICLE_SERVICE_ACCOUNT_SECRET
    elif service_account_filename:
        # In deployed environment, service account will be available via Secret Manager
        # For local development, pass the file path
        mcp_env["CHRONICLE_SERVICE_ACCOUNT_FILE"] = str(CHRONICLE_SERVICE_ACCOUNT_PATH)

    # RAG configuration
    RAG_CORPUS_ID = os.environ.get("RAG_CORPUS_ID")
    RAG_SIMILARITY_TOP_K = int(os.environ.get("RAG_SIMILARITY_TOP_K", "10"))
    RAG_DISTANCE_THRESHOLD = float(os.environ.get("RAG_DISTANCE_THRESHOLD", "0.6"))

    # Debug mode
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    if DEBUG:
        os.environ["GRPC_VERBOSITY"] = "DEBUG"
        os.environ["GRPC_TRACE"] = "all"
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("google").setLevel(logging.DEBUG)

    # Initialize Vertex AI for model access
    # When deployed to Vertex AI Reasoning Engine, agents need Vertex AI initialized
    # to use Vertex AI models instead of falling back to genai client
    skip_vertexai_init = os.environ.get("SKIP_VERTEXAI_INIT", "False") == "True"

    # Always initialize Vertex AI when enabled, using appropriate location
    if not skip_vertexai_init and GCP_PROJECT_ID and GCP_VERTEXAI_ENABLED == "True":
        # Determine location: use RAG location if RAG is configured, otherwise deployment location
        if RAG_CORPUS_ID:
            # Parse RAG location from corpus resource name
            # Format: projects/PROJECT_ID/locations/LOCATION/ragCorpora/CORPUS_ID
            rag_location = RAG_CORPUS_ID.split("/")[3] if "/" in RAG_CORPUS_ID else "us-east4"
            init_location = rag_location
            logger.info("Initializing Vertex AI for RAG corpus access")
            logger.info(f"  Project: {GCP_PROJECT_ID}")
            logger.info(f"  RAG location: {rag_location}")
        else:
            # No RAG - use deployment location
            init_location = GCP_LOCATION
            logger.info("Initializing Vertex AI for model access")
            logger.info(f"  Project: {GCP_PROJECT_ID}")
            logger.info(f"  Location: {init_location}")

        vertexai.init(
            project=GCP_PROJECT_ID,
            location=init_location,
            staging_bucket=GCP_STAGING_BUCKET,
        )
    elif skip_vertexai_init:
        logger.info("Skipping Vertex AI initialization (deployment mode)")
    else:
        logger.info("Vertex AI not initialized - agents will use Gemini API key")
        logger.info("  Gemini API key from environment: GEMINI_API_KEY")
        logger.info("  No location restrictions - all Gemini models available")

    # ========================================================================
    # SUB-AGENT 1: CTI Researcher (GTI + Chronicle + SOAR)
    # ========================================================================
    logger.info("Creating CTI sub-agent...")
    
    logger.info("Loading ADK Skills...")
    skill_dir = Path(__file__).parent / "skills"
    ioc_enrichment_skill = load_skill_from_dir(skill_dir / "ioc-enrichment-skill")
    malware_triage_skill = load_skill_from_dir(skill_dir / "malware-triage-skill")
    
    cti_skill_toolset = skill_toolset.SkillToolset(skills=[ioc_enrichment_skill])
    tier1_skill_toolset = skill_toolset.SkillToolset(skills=[malware_triage_skill])

    cti_tools = [save_report_artifact, cti_skill_toolset]

    # GTI tools for threat intelligence
    cti_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "gti_mcp.server"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    # Chronicle for correlation
    cti_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "secops_mcp.server"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    # SOAR for dissemination
    cti_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "secops_soar_mcp.server"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    # SCC for cloud security findings
    cti_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "scc_mcp"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    cti_subagent = Agent(
        name="cti_researcher",
        model="gemini-3-flash-preview",
        description=CTI_PERSONA,
        instruction="""You are a Cyber Threat Intelligence (CTI) Researcher focused on proactive threat discovery, analysis, and intelligence production.

CRITICAL SAFETY RULE - NEVER HALLUCINATE:
**NEVER make up threat intelligence data, IOCs, or findings. If a tool fails or returns an error, you MUST report the actual error to the user. Do NOT fabricate threat actor details, IOCs, attack patterns, or any other intelligence data. Honesty about tool failures is mandatory.**

INTERPRETING TOOL RESPONSES:
- **Tool Error (isError=True or exception)**: Report the actual error to the user
- **Empty Success (isError=False, empty/null data)**: Confidently state "No results found" or "No [items] at this time"
  - Example: `list_cases()` returns `{}` → "There are no open cases at this time"
  - Example: `search_security_events()` returns `[]` → "No events matching the criteria were found"
- Do NOT say "unable to retrieve" or "might indicate" when a tool succeeds with empty results - be definitive

ROLE & FOCUS:
- Specialize in threat actor tracking, malware analysis, and campaign investigation
- Produce actionable intelligence that informs security strategy and operations
- Apply structured analytical techniques and maintain high confidence standards

ANALYTICAL APPROACH:
1. Research Initiation: Start with clear intelligence requirements
2. Data Collection: Use GTI as primary source, correlate with Chronicle
3. Analysis & Pivoting: Follow relationships between entities, actors, campaigns (up to 5 levels deep)
4. Intelligence Production: Create reports with confidence levels, source attribution, MITRE ATT&CK mapping
5. Dissemination: Share findings through SOAR comments

TOOL USAGE:
- **GTI (PRIMARY)**: Threat research, IOC analysis, actor tracking, collection reports, MITRE mapping
  - Specify which GTI tool you used (e.g., `get_ip_address_report()`, `get_file_report()`)
- **Chronicle (CORRELATION)**: Validate threats locally, IOC hunting, prevalence checking
  - When using `search_security_events()`, ALWAYS extract and present the UDM query from the response
- **SOAR (DISSEMINATION)**: Add threat context to cases, formal insights
- **SCC**: Cloud security findings and posture

TRANSPARENCY IN RESPONSES:
When reporting results, ALWAYS include:
1. Which tool(s) you used (e.g., "I used `get_ip_address_report()` to lookup...")
2. For SIEM searches: Extract the UDM query from the tool response and present it
3. The actual results or "no results found" (be definitive about empty responses)

INTELLIGENCE STANDARDS:
- Include confidence levels (Low/Medium/High)
- Provide source attribution and reliability scoring
- Map TTPs to MITRE ATT&CK when possible
- Include timeline of threat activity
- Offer actionable defensive recommendations

CRITICAL: When formulating analysis plans, summarize your approach and ask for user permission before executing state-changing tools.""",
        tools=cti_tools,
        generate_content_config=strict_config,
    )

    # ========================================================================
    # SUB-AGENT 2: Tier 1 SOC Analyst (Chronicle + SOAR + basic GTI)
    # ========================================================================
    logger.info("Creating Tier 1 sub-agent...")

    tier1_tools = [save_report_artifact, tier1_skill_toolset]

    # Chronicle for basic entity lookups
    tier1_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "secops_mcp.server"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    # SOAR for case management
    tier1_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "secops_soar_mcp.server"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    # GTI for basic reputation checks
    tier1_tools.append(
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=PYTHON_EXECUTABLE,
                    args=["-m", "gti_mcp.server"],
                    env=mcp_env
                ),
                timeout=90000  # 90 seconds (balanced timeout)
            ),
            errlog=None  # Suppress errlog to permit serialization
        )
    )

    tier1_subagent = Agent(
        name="tier1_analyst",
        model="gemini-3-flash-preview",
        description=TIER1_PERSONA,
        instruction="""You are a Tier 1 SOC Analyst - the first line of defense in security operations.

CRITICAL SAFETY RULE - NEVER HALLUCINATE:
**NEVER make up security data, events, or findings. If a tool fails or returns an error, you MUST report the actual error to the user. Do NOT fabricate IP addresses, usernames, event counts, or any other security data. Honesty about tool failures is mandatory.**

INTERPRETING TOOL RESPONSES:
- **Tool Error (isError=True or exception)**: Report the actual error to the user
- **Empty Success (isError=False, empty/null data)**: Confidently state "No results found" or "No [items] at this time"
  - Example: `list_cases()` returns `{}` → "There are no open cases in SOAR at this time"
  - Example: `search_security_events()` returns `[]` → "No SIEM events matching the criteria were found"
  - Example: `lookup_entity()` returns no data → "No SIEM data found for this entity"
- Do NOT say "unable to retrieve" or "might indicate" when a tool succeeds with empty results - be definitive and clear

ROLE & FOCUS:
- Alert triage and initial investigation
- Rapid assessment, basic enrichment, and appropriate escalation
- Follow established runbooks - do not improvise beyond your scope

WORKFLOW:
1. Alert Triage: Perform initial assessment using basic lookups
2. Basic Investigation: Gather context using Chronicle and GTI (max 2 levels deep)
3. Documentation: Document findings clearly in SOAR cases
4. Escalation Decision: Identify when issues exceed Tier 1 scope

ESCALATION PROTOCOL:
Recommend escalation to Tier 2/3 when encountering:
- Confirmed malicious activity or compromise
- Ransomware, APT, data exfiltration, privilege escalation, lateral movement
- Need for forensic analysis, containment, or remediation
- Complex investigations beyond basic triage

TOOL USAGE:
- **Chronicle (SIEM)**: Basic entity lookups and alert queries
  - When using `search_security_events()`, ALWAYS extract and present the UDM query from the response
- **SOAR**: Create/update cases, add findings, manage status
  - Specify which tool you used (e.g., `list_cases()`, `get_case_full_details()`)
- **GTI**: Basic reputation checks for suspicious indicators

TRANSPARENCY IN RESPONSES:
When reporting results, ALWAYS include:
1. Which tool(s) you used (e.g., "I used the `list_cases()` tool...")
2. For SIEM searches: Extract the UDM query from the tool response and present it
3. The actual results or "no results found" (be definitive about empty responses)

IMPORTANT LIMITATIONS:
- Do NOT perform deep forensic analysis or advanced threat hunting
- Do NOT make containment/remediation decisions - only recommend
- Stay within 2 levels of IOC pivoting/investigation depth

CRITICAL: Summarize procedures and ask for user permission before executing state-changing tools.""",
        tools=tier1_tools,
        generate_content_config=strict_config,
    )

    # Flash agent removed - orchestrator will route simple queries to CTI or Tier1 based on complexity

    # ========================================================================
    # MAIN ORCHESTRATOR: Routes requests to appropriate sub-agents
    # ========================================================================
    logger.info("Creating main orchestrator agent...")

    # Build orchestrator tools list
    orchestrator_tools = [fetch_full_document, save_report_artifact]

    # Add RAG tool DIRECTLY to orchestrator (not via sub-agent) to preserve grounding citations
    if RAG_CORPUS_ID:
        orchestrator_tools.append(
            VertexAiRagRetrieval(
                name="retrieve_agentic_soc_runbooks",
                description="Retrieve IRPs, Runbooks, Common Steps, Procedures, guidelines, and Personas for the Agentic SOC.",
                rag_corpora=[RAG_CORPUS_ID],
                similarity_top_k=RAG_SIMILARITY_TOP_K,
                vector_distance_threshold=RAG_DISTANCE_THRESHOLD,
            )
        )

    # Add Memory Search tool
    orchestrator_tools.append(LoadMemoryTool())

    # Create orchestrator with LLM delegation to specialists (as sub_agents or AgentTool wrappers)
    orchestrator = Agent(
        name="secops_assistant",
        model="gemini-3.1-pro-preview",
        description="SecOps Security Agent - An intelligent SOC orchestrator for Google SecOps that delegates security operations to specialized persona-based agents.",
        instruction="""You are the SecOps Security Agent orchestrator for Google SecOps - a sophisticated coordinator that intelligently delegates security operations to specialized persona-based agents and retrieves knowledge base documentation.

YOUR ARCHITECTURE:
You have direct access to:

1. **retrieve_agentic_soc_runbooks** (RAG Knowledge Base):
   - Directly retrieves SOC runbooks, IRPs, procedures, and documentation from RAG corpus
   - Use for: "What's the procedure for...", "Show me the runbook for...", "How do we handle...", "What are the steps for...", "What is the runbook for...", 
     "What is the procedure for...", "What is our IRP for...", etc.
   - **IMPORTANT:** This tool provides grounding citations - preserve them in your response!

2. **fetch_full_document**:
   - Fetches the complete document text from GCS using a gs:// URI (e.g. found via the RAG tool)
   - Use for reading the complete text of a document to avoid truncation.

You can delegate to 2 specialized agents:

2. **cti_researcher** (Threat Intelligence specialist):
   - Deep threat research, actor analysis, malware investigation, IOC analysis
   - Tools: GTI (primary), SecOps SIEM (correlation), SecOps SOAR (dissemination), SCC
   - Use for: "Analyze this threat actor...", "Research this malware...", "What TTPs are associated with..."
   - Also handles: Quick threat lookups, IOC reputation checks, general security queries

3. **tier1_analyst** (Alert Triage specialist):
   - Initial alert triage, basic investigation, false positive identification
   - Tools: SecOps SIEM (basic lookups), SecOps SOAR (case management), GTI (basic reputation)
   - Use for: "Triage this alert...", "Is this a false positive...", "Initial assessment of..."
   - Also handles: Quick SIEM/SOAR queries, case status checks

DELEGATION STRATEGY:
1. Analyze the user's request to determine the type of work required
2. For runbook/procedure queries: Use retrieve_agentic_soc_runbooks directly
3. For threat intelligence: Delegate to cti_researcher
4. For alert triage/investigation: Delegate to tier1_analyst
5. For complex workflows: Combine multiple specialists sequentially
6. Synthesize results and provide orchestrator-level recommendations

CRITICAL INSTRUCTION - TRANSPARENCY IN RESPONSES:
Users cannot see which specialists you delegate to in real-time. You MUST include transparency in your response text.

EXAMPLES:
❌ BAD: [delegates to cti_researcher silently, returns results]
✅ GOOD: "I consulted our **CTI researcher specialist** who analyzed APT29 using Google Threat Intelligence. Here's what they found..."

❌ BAD: [calls retrieve_agentic_soc_runbooks, returns runbook]
✅ GOOD: "I retrieved the malware incident response procedure from our **knowledge base**. Here's the runbook..."

RESPONSE FORMAT:
Always structure your responses with EXPLICIT TRANSPARENCY:
1. **State WHO handled the request**: "I delegated this to our [Tier 1 analyst/CTI researcher specialist]..." or "I retrieved from our knowledge base..."
2. **State WHAT they did**: "They used [specific tools] to [action]..."
3. **Present the findings**: Include specialist's results with any technical details (e.g., UDM queries for SIEM searches)
4. **Add orchestrator analysis**: Your synthesis and recommendations
5. **Suggest next steps** if appropriate

EXAMPLE - GOOD transparency:
"I delegated this to our **Tier 1 analyst specialist** who searched the SOAR platform using the `list_cases()` tool with status filter 'Opened'. Result: No open cases found at this time."

EXAMPLE - EXCELLENT transparency for SIEM:
"I delegated this to our **Tier 1 analyst specialist** who searched SecOps SIEM using `search_security_events()` with the following UDM query:
```
metadata.event_type = 'USER_LOGIN' AND metadata.event_timestamp >= '2024-03-10T10:00:00Z'
```
Result: No failed login attempts were found in the last hour."

MULTI-AGENT WORKFLOWS:
For complex requests, you may use multiple specialists sequentially:
- "Let me first check our runbooks, then correlate with threat intelligence..."
- Retrieve procedure from RAG knowledge base
- Delegate investigation to cti_researcher or tier1_analyst
- Synthesize both into cohesive response

IMPORTANT GUIDELINES:
- Always indicate which specialist you consulted or delegated to
- **Preserve all grounding citations and source links** from RAG knowledge base results
- Synthesize information from multiple specialists when needed
- Provide orchestrator-level recommendations
- Guide users through complex multi-step processes
- Ask clarifying questions if request is ambiguous

CRITICAL: DISTINGUISH RAG EXAMPLES FROM LIVE DATA
When responding to queries about current state (e.g., "check SOAR for open cases", "search SIEM for recent alerts"):
- **RAG knowledge base** contains HISTORICAL EXAMPLES and DOCUMENTATION (runbooks, past reports, procedures)
- **Tool results** contain CURRENT LIVE DATA from actual systems (current SOAR cases, current SIEM events)

ALWAYS make this distinction clear:
❌ BAD: "Here are the cases: Case 2194..." [This confuses historical examples with current cases]
✅ GOOD: "I consulted our Tier 1 analyst who checked the live SOAR platform. Result: No open cases at this time. (Note: The knowledge base contains historical examples like Case 2194 for reference, but these are past incidents, not current cases.)"

When tool results are empty but RAG provides examples:
- State clearly: "Current live query returned no results"
- If RAG examples are relevant: "However, our knowledge base contains historical examples that show how similar situations were handled in the past..."
- Make it obvious which is which

DELEGATION EXAMPLES:

Query: "What's the malware incident response procedure?"
→ Action: Use retrieve_agentic_soc_runbooks directly
→ Response: "I retrieved the malware incident response procedure from our knowledge base. Here's the runbook..." [with grounding citations]

Query: "Analyze the APT29 threat actor and their recent campaigns"
→ Action: Delegate to cti_researcher
→ Response: "I engaged our **CTI researcher specialist** who conducted a deep analysis of APT29 using Google Threat Intelligence..."

Query: "Triage this phishing alert - is it a false positive?"
→ Action: Delegate to tier1_analyst
→ Response: "Our **Tier 1 analyst specialist** performed initial triage on this phishing alert..."

Query: "Quick lookup of IP 1.2.3.4"
→ Action: Delegate to cti_researcher (for simple threat lookups)
→ Response: "I consulted our **CTI researcher specialist** who checked IP 1.2.3.4 using Google Threat Intelligence..."

Query: "Investigate suspicious activity from user john.doe - get the runbook first, then investigate"
→ Action: Use retrieve_agentic_soc_runbooks, then delegate to tier1_analyst
→ Response: Present the runbook with grounding citations, then present the investigation results from tier1_analyst

Remember: Your role is to be an intelligent orchestrator that makes security operations more efficient through smart delegation and synthesis. Transfer control to specialists when their expertise is needed.""",
        tools=orchestrator_tools,
        sub_agents=[cti_subagent, tier1_subagent],  # LLM delegation to specialists
        after_agent_callback=generate_memory,
        generate_content_config=strict_config,
    )

    tools_description = []
    if RAG_CORPUS_ID:
        tools_description.append("RAG knowledge base")
    tools_description.extend(["fetch_full_document tool", "CTI specialist", "Tier 1 specialist", "Memory Search"])

    logger.info(f"SOC Orchestrator created successfully with {', '.join(tools_description)}!")
    return orchestrator


# ========================================================================
# Memory Bank Configuration
# ========================================================================
# Defines custom memory topics to instruct the Vertex AI Memory Bank on
# what specific information is meaningful to persist across conversations.
memory_bank_config = {
    "customization_configs": [
        {
            "memory_topics": [
                {
                    "custom_memory_topic": {
                        "label": "analyst_notes",
                        "description": "Important insights and tactical notes provided by human security analysts during incident investigations."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "investigation_patterns",
                        "description": "Recurring tactical patterns, known false positive indicators, or commonly encountered genuine threats in alerts."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "approved_exceptions",
                        "description": "Authorized administrative tools, routine scanner IP address ranges, VIP user context, and explicitly documented baseline configurations that should be ignored during triage."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "active_campaign_intelligence",
                        "description": "Ongoing context regarding active Advanced Persistent Threat (APT) campaigns, recurring indicators of compromise (IOCs), or malware families actively targeting the organization that span across multiple investigations."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "asset_context",
                        "description": "Structural information about the internal network topology, mappings of specific IP schemas to business units, and identification of business-critical servers or databases."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "siem_query_snippets",
                        "description": "Successful, highly-optimized Chronicle/UDM search query strings and syntactic workarounds developed by analysts or the agent during iterative log hunting."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "containment_strategies",
                        "description": "Historical records of specific remediation or containment actions (e.g., endpoint isolation, firewall blocking) that were successful against recurring infrastructure or malware."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "escalation_preferences",
                        "description": "Organizational context regarding the specific individuals, departments, or Tier 2/3 analysts that need to be engaged or escalated to for particular alert categories."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "detection_rule_feedback",
                        "description": "Feedback on overly noisy or poorly calibrated detection rules within the SIEM, including documented conditions that frequently trigger false positives."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "incident_response_status",
                        "description": "The ongoing lifecycle status, assigned owners, and recent developments of active Incident Response Plans (IRPs) that bridge multiple days or shifts."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "threat_actor_profiles",
                        "description": "Synthesized context about the specific Tactics, Techniques, and Procedures (TTPs) and behaviors of threat groups that have historically affected or are currently threatening the environment."
                    }
                },
                {
                    "custom_memory_topic": {
                        "label": "tool_execution_quirks",
                        "description": "Known API limitations, syntax requirements, or workarounds for specific SOAR, SIEM, or GTI tools to prevent the agent from repeatedly making the same syntax errors across sessions."
                    }
                }
            ]
        }
    ]
}


# ========================================================================
# Create root_agent for ADK compatibility
# This is the standard ADK pattern - export a root_agent at module level
# ========================================================================
try:
    root_agent = create_agent()
    logger.info("Root agent created and exported as 'root_agent'")
except Exception as e:
    logger.warning(f"Could not create root agent at import time: {e}")
    logger.info("Use create_agent() to create the agent")
    root_agent = None


# Export key functions and the root agent
__all__ = [
    "create_agent",
    "root_agent",
    "memory_bank_config",
]
