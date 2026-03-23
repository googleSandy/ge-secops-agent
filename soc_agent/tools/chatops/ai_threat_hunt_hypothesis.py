"""
ChatOps Card: ai_threat_hunt_hypothesis
Modernized Version
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-hunt",
      "card": {
        "header": {
          "title": "AI Threat Hunting",
          "subtitle": "New Hypothesis Generated",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/travel_explore/default/48px.svg",
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
                            "topLabel": "Target Environment",
                            "text": "SolarWinds",
                            "startIcon": { "materialIcon": { "name": "dns" } }
                          }
                        }
                      ]
                    },
                    {
                      "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                      "widgets": [
                        {
                          "decoratedText": {
                            "topLabel": "Priority",
                            "text": "Medium",
                            "startIcon": { "materialIcon": { "name": "flag" } }
                          }
                        }
                      ]
                    }
                  ]
                }
              },
              {
                "decoratedText": {
                  "topLabel": "Hunt Logic",
                  "text": "Orphaned credentials / Supply chain attack",
                  "bottomLabel": "Based on recent industry trends & intelligence",
                  "startIcon": { "materialIcon": { "name": "psychology" } }
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Launch Hunt", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Save for later", "onClick": { "openLink": { "url": deny_url } } }
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
    send_card(get_card())
