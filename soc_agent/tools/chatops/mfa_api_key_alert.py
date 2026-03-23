import os
from pathlib import Path
from dotenv import load_dotenv
from card_client import send_card, generate_action_url
"""
ChatOps Card: mfa_api_key_alert
Generated from mfa_api_key_alert.sh
"""

def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    return {
  "cardsV2": [
    {
      "cardId": "mfa-api-key-opt",
      "card": {
        "header": {
          "title": "MFA Verification",
          "subtitle": "New API Key Created",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/vpn_key/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "decoratedText": {
                  "topLabel": "User",
                  "text": "dandye@example.com",
                  "startIcon": {
                    "knownIcon": "PERSON"
                  }
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Approve",
                      "onClick": {
                        "openLink": {
                          "url": generate_action_url("Ok", session_id=session_id, agent_engine_id=agent_engine_id, user_id=user_id)
                        }
                      }
                    },
                    {
                      "text": "Revoke",
                      "onClick": {
                        "openLink": {
                          "url": generate_action_url("No", session_id=session_id, agent_engine_id=agent_engine_id, user_id=user_id)
                        }
                      }
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
