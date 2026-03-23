import os
from pathlib import Path
from dotenv import load_dotenv
from card_client import send_card, generate_action_url

def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    """
    ChatOps Card: triage_report_ready
    Provides a download link for the initial triage report.
    """
    
    download_url = generate_action_url(
        "Download Triage Report", 
        session_id=session_id, 
        agent_engine_id=agent_engine_id, 
        user_id=user_id
    )
    
    acknowledge_url = generate_action_url(
        "Acknowledge and Close", 
        session_id=session_id, 
        agent_engine_id=agent_engine_id, 
        user_id=user_id
    )

    return {
        "cardsV2": [
            {
                "cardId": "triage-report",
                "card": {
                    "header": {
                        "title": "Triage Report Ready",
                        "subtitle": "Analysis complete for INC-2024",
                        "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/description/default/48px.svg",
                        "imageType": "CIRCLE"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "decoratedText": {
                                        "topLabel": "Scan Coverage",
                                        "text": "12 Hosts Triage / 4 Malicious Findings",
                                        "startIcon": { "materialIcon": { "name": "analytics" } }
                                    }
                                },
                                {
                                    "decoratedText": {
                                        "topLabel": "Time to Generate",
                                        "text": "2 minutes, 14 seconds",
                                        "startIcon": { "materialIcon": { "name": "timer" } }
                                    }
                                },
                                {
                                    "buttonList": {
                                        "buttons": [
                                            {
                                                "text": "Download Full PDF",
                                                "color": { "red": 0, "green": 0.4, "blue": 1.0 },
                                                "onClick": { "openLink": { "url": download_url } }
                                            },
                                            {
                                                "text": "Acknowledge",
                                                "onClick": { "openLink": { "url": acknowledge_url } }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }

if __name__ == "__main__":
    # Load environment for manual testing
    load_dotenv(Path(__file__).parent.parent.parent.parent / ".env")
    
    session_id = os.getenv("CHATOPS_TEST_SESSION_ID", "test-session")
    agent_id = os.getenv("AGENT_ENGINE_RESOURCE_NAME", "test-agent")
    
    # Send the card
    card = get_card(
        session_id=session_id, 
        agent_engine_id=agent_id, 
        user_id="vais-query-reasoning-engine"
    )
    send_card(card)
