"""
ChatOps Card: ai_firewall_bypass_request
Modernized Version
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-fw",
      "card": {
        "header": {
          "title": "AI Agent Request",
          "subtitle": "Temporary Firewall Bypass",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/shield_with_house/default/48px.svg",
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
                            "topLabel": "Source",
                            "text": "Isolated-VLAN-9",
                            "startIcon": { "materialIcon": { "name": "block" } }
                          }
                        }
                      ]
                    },
                    {
                      "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                      "widgets": [
                        {
                          "decoratedText": {
                            "topLabel": "Target",
                            "text": "Analysis Bucket",
                            "startIcon": { "materialIcon": { "name": "storage" } }
                          }
                        }
                      ]
                    }
                  ]
                }
              },
              {
                "decoratedText": {
                  "topLabel": "Network Policy",
                  "text": "Allow Port 443 (Egress)",
                  "bottomLabel": "Duration: 10 minutes",
                  "startIcon": { "materialIcon": { "name": "vpn_lock" } }
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Approve (10m)",
                      "color": { "red": 0, "green": 0.6, "blue": 0 },
                      "onClick": { "openLink": { "url": "https://example.com/approve" } }
                    },
                    {
                      "text": "Deny Request",
                      "color": { "red": 0.8, "green": 0, "blue": 0 },
                      "onClick": { "openLink": { "url": "https://example.com/deny" } }
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
