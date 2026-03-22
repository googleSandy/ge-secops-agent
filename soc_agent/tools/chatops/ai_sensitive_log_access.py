"""
ChatOps Card: ai_sensitive_log_access
Generated from ai_sensitive_log_access.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-logs",
      "card": {
        "header": {
          "title": "AI Data Request",
          "subtitle": "Privileged Logs Required",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/policy/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "To continue investigating the insider threat, I need temporary access to <b>HR Personal Data</b> logs. This is outside my default scope."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Grant (1 Hour)",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/grant"
                        }
                      }
                    },
                    {
                      "text": "Reject Request",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/no"
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
    card = get_card()
    send_card(card)
