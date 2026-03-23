import logging
import os

import httpx
from typing import Optional
import importlib
from google.adk.agents.context import Context
from soc_agent.tools.chatops.card_client import generate_action_url


logger = logging.getLogger(__name__)


def _get_context_ids(ctx: Optional[Context] = None) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extracts session_id, agent_engine_id, and user_id from the ADK Context and environment variables.
    Handles quote stripping and fallback logic for Playground testing.
    """
    session_id = None
    
    # 1. Provide safe extraction for AGENT_ENGINE_ID (quote stripping)
    agent_engine_id = os.environ.get("AGENT_ENGINE_RESOURCE_NAME")
    if agent_engine_id:
        agent_engine_id = agent_engine_id.strip("'").strip('"')
        
    # 2. Extract Session ID (with liberal logging for debug)
    if ctx:
        logger.info(f"[CHATOPS DEBUG] Inspecting Context object: dir={dir(ctx)}")
        if hasattr(ctx, "session"):
            logger.info(f"[CHATOPS DEBUG] Found ctx.session. Type={type(ctx.session)}, Value={ctx.session}")
            if hasattr(ctx.session, "id"):
                session_id = ctx.session.id
            elif isinstance(ctx.session, str) and ctx.session:
                session_id = ctx.session
                
            if not agent_engine_id and hasattr(ctx.session, "app_name") and ctx.session.app_name:
                agent_engine_id = ctx.session.app_name
                logger.info(f"[CHATOPS DEBUG] Natively resolved agent_engine_id from ADK session: {agent_engine_id}")
        elif hasattr(ctx, "_invocation_context"):
            logger.info(f"[CHATOPS DEBUG] Found ctx._invocation_context. Inspecting...")
            if hasattr(ctx._invocation_context, "session"):
                if hasattr(ctx._invocation_context.session, "id"):
                    session_id = ctx._invocation_context.session.id
                elif isinstance(ctx._invocation_context.session, str):
                    session_id = ctx._invocation_context.session

                if not agent_engine_id and hasattr(ctx._invocation_context.session, "app_name") and ctx._invocation_context.session.app_name:
                    agent_engine_id = ctx._invocation_context.session.app_name
                    logger.info(f"[CHATOPS DEBUG] Natively resolved agent_engine_id from ADK context wrapper: {agent_engine_id}")

        if not session_id:
            logger.warning(f"[CHATOPS DEBUG] Failed to extract session_id! Dumping full Context __dict__: {getattr(ctx, '__dict__', 'No __dict__')}")
            
    # 3. Extract User ID with Fallback
    user_id = None
    if ctx and hasattr(ctx, "user_id") and ctx.user_id:
         user_id = ctx.user_id
    else:
         # Fallback for Playground identity lock compliance
         user_id = "vais-query-reasoning-engine"
         
    return session_id, agent_engine_id, user_id


async def send_raw_card(payload: dict) -> str:
    """
    Sends a complete raw JSON card payload to the configured Google Chat webhook asynchronously.
    """
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        logger.error("WEBHOOK_URL environment variable is not set.")
        return "Error: WEBHOOK_URL environment variable is not set."

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json; charset=UTF-8"},
            )
            response.raise_for_status()
            logger.info("Raw ChatOps card sent successfully.")
            return f"Successfully sent ChatOps card. (Status: {response.status_code})"
    except Exception as e:
        logger.error(f"Failed to send raw ChatOps card: {e}")
        return f"Error sending ChatOps card: {str(e)}"


async def dispatch_card(template_name: str, ctx: Optional[Context], **kwargs) -> str:
    """
    Dynamically loads and dispatches a Google Chat card from the chatops library.
    
    Args:
        template_name: The name of the python module in soc_agent.tools.chatops (without .py)
        ctx: ADK Context to extract session and user IDs
        **kwargs: Dynamic variables to pass to the card's get_card() function.
    """
    try:
        module = importlib.import_module(f"soc_agent.tools.chatops.{template_name}")
        if not hasattr(module, "get_card"):
            return f"Error: Template '{template_name}' does not implement get_card()."
            
        session_id, agent_engine_id, user_id = _get_context_ids(ctx)
        
        # Inject standard context args securely
        kwargs["session_id"] = session_id
        kwargs["agent_engine_id"] = agent_engine_id
        kwargs["user_id"] = user_id
        
        # All modern cards return a full `{"cardsV2": [...]}` dict
        card_content = module.get_card(**kwargs)
        
        return await send_raw_card(card_content)
        
    except ImportError:
        return f"Error: Card template '{template_name}' not found."
    except Exception as e:
        logger.error(f"Failed to dispatch card {template_name}: {e}")
        return f"Error dispatching card: {e}"


async def verify_user_travel(user_email: str, location: str, arrival_time: str, ctx: Context = None) -> str:
    """
    Sends an impossible travel confirmation card to a user.
    Uses the 'traveler_confirmation' template.
    
    Args:
        user_email: The email of the affected user.
        location: The suspicious travel location.
        arrival_time: When the login occurred.
        ctx: The ADK context (injected automatically).
    """
    return await dispatch_card(
        "traveler_confirmation", 
        ctx, 
        user_email=user_email, 
        location=location, 
        arrival_time=arrival_time
    )

async def request_triage_approval(finding_summary: str, target_system: str, ctx: Context = None) -> str:
    """
    Sends an approval card to human analysts for host isolation.
    Uses the 'host_isolation_approval' template.
    
    Args:
        finding_summary: Why this system needs isolation.
        target_system: The hostname or IP to isolate.
        ctx: The ADK context (injected automatically).
    """
    return await dispatch_card(
        "host_isolation_approval", 
        ctx, 
        finding_summary=finding_summary, 
        target_system=target_system
    )

async def deliver_report(case_id: str, report_summary: str, ctx: Context = None) -> str:
    """
    Sends a card indicating a triage report is ready for download.
    Uses the 'triage_report_ready' template.
    
    Args:
        case_id: The ID of the investigation.
        report_summary: A brief summary of the findings.
        ctx: The ADK context (injected automatically).
    """
    return await dispatch_card(
        "triage_report_ready", 
        ctx, 
        case_id=case_id, 
        report_summary=report_summary
    )

async def generic_notification(card_template_name: str, ctx: Context = None, **kwargs) -> str:
    """
    Sends any existing chatops card template by name.
    
    Args:
        card_template_name: The name of the python module (e.g. 'impossible_travel_alert' or 'ai_stale_account_cleanup').
        ctx: The ADK Context (injected automatically).
        **kwargs: Must include any keyword arguments the target card's get_card() expects.
    """
    return await dispatch_card(card_template_name, ctx, **kwargs)


async def send_chatops_card(
    title: str,
    subtitle: str,
    sections: list[dict],
    card_id: str = "soc-agent-alert",
    image_url: str = "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/security/default/48px.svg",
) -> str:
    """
    Sends a rich V2 card to the configured ChatOps webhook (Google Chat).

    Args:
        title: The title of the card header.
        subtitle: The subtitle of the card header.
        sections: A list of card section dictionaries. Each section can contain widgets (textParagraph, decoratedText, buttonList).
        card_id: Unique ID for the card (optional).
        image_url: URL for the header icon (optional).
    """
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        logger.error("WEBHOOK_URL environment variable is not set.")
        return "Error: WEBHOOK_URL environment variable is not set. Please configure it in .env."

    payload = {
        "cardsV2": [
            {
                "cardId": card_id,
                "card": {
                    "header": {
                        "title": title,
                        "subtitle": subtitle,
                        "imageUrl": image_url,
                        "imageType": "CIRCLE",
                    },
                    "sections": sections,
                },
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json; charset=UTF-8"},
            )
            response.raise_for_status()
            logger.info(f"ChatOps card sent successfully: {card_id}")
            return f"Successfully sent ChatOps card to human analyst. (Status: {response.status_code})"
    except Exception as e:
        logger.error(f"Failed to send ChatOps card: {e}")
        return f"Error sending ChatOps card: {str(e)}"


async def request_human_confirmation(
    action_name: str,
    description: str,
    context_data: str,
    ctx: Context = None,
    approval_url: str = None,
    deny_url: str = None,
) -> str:
    """
    Sends a request for human-in-the-loop confirmation via ChatOps.
    If 'ctx' is available, it will generate secure signed URLs for the action.

    Args:
        action_name: The name of the action requiring confirmation (e.g. 'Block IP', 'Isolate Host').
        description: Why this action is being proposed.
        context_data: Relevant data snippets (e.g. IP address, hostname, alert ID).
        ctx: ADK Context (automatically injected).
        approval_url: Override URL to approve (optional).
        deny_url: Override URL to deny (optional).
    """
    # Auto-resolve session and agent IDs from context utilizing the new secure helper
    session_id, agent_engine_id, user_id = _get_context_ids(ctx)

    # Generate signed URLs if not explicitly provided
    if not approval_url:
        approval_url = generate_action_url(f"Approve {action_name}", session_id, agent_engine_id, user_id=user_id)
    if not deny_url:
        deny_url = generate_action_url(f"Deny {action_name}", session_id, agent_engine_id, user_id=user_id)

    sections = [
        {
            "header": "Action Required",
            "widgets": [
                {
                    "decoratedText": {
                        "topLabel": "Proposed Action",
                        "text": action_name,
                        "startIcon": {"knownIcon": "STAR"},
                    }
                },
                {"textParagraph": {"text": f"<b>Rationale:</b> {description}"}},
                {
                    "decoratedText": {
                        "topLabel": "Context",
                        "text": context_data,
                        "startIcon": {"knownIcon": "BOOKMARK"},
                    }
                },
            ],
        },
        {
            "widgets": [
                {
                    "buttonList": {
                        "buttons": [
                            {
                                "text": "Approve",
                                "onClick": {"openLink": {"url": approval_url}},
                            },
                            {
                                "text": "Deny",
                                "onClick": {"openLink": {"url": deny_url}},
                            },
                        ]
                    }
                }
            ]
        },
    ]

    return await send_chatops_card(
        title="Human Confirmation Required",
        subtitle="Agent proposing state-changing action",
        sections=sections,
        card_id=f"confirm-{action_name.lower().replace(' ', '-')}",
        image_url="https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/contact_support/default/48px.svg",
    )


async def notify_human_incident(
    incident_id: str, severity: str, summary: str, chronicle_link: str = None
) -> str:
    """
    Notifies a human analyst about a new high-priority incident.

    Args:
        incident_id: The ID of the incident.
        severity: Severity level (e.g. CRITICAL, HIGH).
        summary: Short summary of the incident.
        chronicle_link: Link to the investigation in Chronicle (optional).
    """
    widgets = [
        {
            "decoratedText": {
                "topLabel": "Incident ID",
                "text": incident_id,
                "startIcon": {"knownIcon": "TICKET"},
            }
        },
        {
            "decoratedText": {
                "topLabel": "Severity",
                "text": severity,
                "startIcon": {"knownIcon": "STALKER"},
            }
        },
        {"textParagraph": {"text": f"<b>Summary:</b> {summary}"}},
    ]

    if chronicle_link:
        widgets.append(
            {
                "buttonList": {
                    "buttons": [
                        {
                            "text": "View in Chronicle",
                            "onClick": {"openLink": {"url": chronicle_link}},
                        }
                    ]
                }
            }
        )

    sections = [{"widgets": widgets}]

    return await send_chatops_card(
        title="Critical Incident Notification",
        subtitle=f"Automated Alert: {severity}",
        sections=sections,
        card_id=f"incident-{incident_id}",
        image_url="https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/error/default/48px.svg",
    )
