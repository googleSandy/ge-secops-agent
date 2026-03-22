"""
ChatOps Card: ai_brute_force_source_block
Modernized Version
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-fw-block",
      "card": {
        "header": {
          "title": "AI Auto-Defender",
          "subtitle": "Persistent Bot Identification",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/security_update_warning/default/48px.svg",
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
                            "topLabel": "Source IP",
                            "text": "185.x.x.x",
                            "startIcon": { "materialIcon": { "name": "public" } }
                          }
                        }
                      ]
                    },
                    {
                      "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                      "widgets": [
                        {
                          "decoratedText": {
                            "topLabel": "Failed Logins",
                            "text": "5,000",
                            "startIcon": { "materialIcon": { "name": "report_problem" } }
                          }
                        }
                      ]
                    }
                  ]
                }
              },
              {
                "textParagraph": {
                  "text": "This IP has exhibited persistent bot-like behavior across multiple tenants. Action is required to prevent further brute force attempts."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Global Blacklist",
                      "color": { "red": 0.8, "green": 0, "blue": 0 },
                      "onClick": { "openLink": { "url": "https://example.com/ban" } }
                    },
                    {
                      "text": "Ignore",
                      "onClick": { "openLink": { "url": "https://example.com/no" } }
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
