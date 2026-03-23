import os
from pathlib import Path
from dotenv import load_dotenv
from card_client import send_card, generate_action_url

def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    """
    ChatOps Card: host_isolation_approval
    Modernized Version
    """
    
    isolate_url = generate_action_url(
        "Isolate Host Now", 
        session_id=session_id, 
        agent_engine_id=agent_engine_id, 
        user_id=user_id
    )
    
    ignore_url = generate_action_url(
        "Ignore Alert (False Positive)", 
        session_id=session_id, 
        agent_engine_id=agent_engine_id, 
        user_id=user_id
    )

    return {
    "cardsV2": [
      {
        "cardId": "host-iso",
        "card": {
          "header": {
            "title": "Containment Required",
            "subtitle": "Active Infection Confirmed",
            "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/block/default/48px.svg",
            "imageType": "CIRCLE"
          },
          "sections": [
            {
              "widgets": [
                {
                  "columns": {
                    "columnItems": [
                      {
                        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                        "widgets": [
                          {
                            "decoratedText": {
                              "topLabel": "Host Name",
                              "text": "DESKTOP-8291",
                              "startIcon": { "materialIcon": { "name": "computer" } }
                            }
                          }
                        ]
                      },
                      {
                        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                        "widgets": [
                          {
                            "decoratedText": {
                              "topLabel": "Network segment",
                              "text": "Finance-VLAN",
                              "startIcon": { "materialIcon": { "name": "hub" } }
                            }
                          }
                        ]
                      }
                    ]
                  }
                },
                {
                    "decoratedText": {
                        "topLabel": "Detection Status",
                        "text": "<font color=\"#ff0000\">Active C2 identified</font>",
                        "bottomLabel": "Confirmed via SIEM/EDR logs",
                        "startIcon": { "materialIcon": { "name": "security" } }
                    }
                },
                {
                  "buttonList": {
                    "buttons": [
                      {
                        "text": "Isolate Host Now",
                        "color": { "red": 0.8, "green": 0, "blue": 0 },
                        "onClick": { "openLink": { "url": isolate_url } }
                      },
                      {
                        "text": "Ignore (False Positive)",
                        "onClick": { "openLink": { "url": ignore_url } }
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
