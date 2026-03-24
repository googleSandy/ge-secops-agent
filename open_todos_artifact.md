# Open ToDos and Open Tasks Artifact

## 1. `ToDo.md` Open Tasks
*   **Critical Incident Notification:** The image is reportedly missing next to the severity label in the card. Located in `soc_agent/tools/chatops_tools.py` where a `warning` icon URL is used for the `startIcon` in the `decoratedText` widget, but it may not be rendering as expected.
*   **Triage Report Ready Card:** The "Download Full PDF" button currently points to a Cloud Function URL (or fallback) instead of a pre-signed GCS URL from the archive. Logic in `soc_agent/tools/chatops/triage_report_ready.py` attempts to generate a signed URL, but it might need refinement to ensure it's pointing to the correct archive location.

## 2. Implementation Plan: Memory Call-outs
The `implementation_plan.md` outlines a large-scale task to update markdown files in `adk_runbooks/rules-bank/` with dynamic memory call-outs:
*   **Automated Baseline Update:** A script is needed to inject "Query Memory" and "Save Memory" steps into all runbooks.
*   **Specialized Manual Updates:** Nuanced call-outs are needed for complex playbooks like IRPs.
*   **Topic Consolidation:** Pending question about whether to keep 12 memory topics or consolidate them down to 10.

## 3. Inline TODOs in Codebase
Found **26 inline TODO comments** in the codebase, notably:
*   `soc_agent/tools/cti_facade.py`: How to invoke `McpToolset` functions programmatically.
*   `pyproject.toml`: Add timeouts to requests in the future.
*   Various logging and performance improvements in the `mcp-security` submodules.
