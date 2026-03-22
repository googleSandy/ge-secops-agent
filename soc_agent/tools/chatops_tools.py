import logging
import os

import httpx


logger = logging.getLogger(__name__)


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
    approval_url: str = "https://example.com/approve",
    deny_url: str = "https://example.com/deny",
) -> str:
    """
    Sends a request for human-in-the-loop confirmation via ChatOps.

    Args:
        action_name: The name of the action requiring confirmation (e.g. 'Block IP', 'Isolate Host').
        description: Why this action is being proposed.
        context_data: Relevant data snippets (e.g. IP address, hostname, alert ID).
        approval_url: URL the human should click to approve (optional).
        deny_url: URL the human should click to deny (optional).
    """
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
