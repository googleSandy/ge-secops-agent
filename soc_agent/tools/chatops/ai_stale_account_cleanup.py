"""
ChatOps Card: ai_stale_account_cleanup
Generated from ai_stale_account_cleanup.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-stale",
      "card": {
        "header": {
          "title": "AI Hygiene Bot",
          "subtitle": "Stale Account Cleanup",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/person_off/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I found 12 accounts with no logins in >90 days. I recommend disabling them immediately to reduce attack surface."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Disable All (12)",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/kill"
                        }
                      }
                    },
                    {
                      "text": "Notify Owners",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/ask"
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
