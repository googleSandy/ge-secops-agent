"""
ChatOps Card: ai_threat_hunt_hypothesis
Modernized Version
"""
from card_client import send_card

def get_card():
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
                    {
                      "text": "Launch Hunt",
                      "color": { "red": 0.1, "green": 0.5, "blue": 1.0 },
                      "onClick": { "openLink": { "url": "https://example.com/hunt" } }
                    },
                    {
                      "text": "Save for later",
                      "onClick": { "openLink": { "url": "https://example.com/save" } }
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
    send_card(get_card())
