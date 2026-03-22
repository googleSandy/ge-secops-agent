"""
ChatOps Card: ai_credential_reset_approval
Generated from ai_credential_reset_approval.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-pwd",
      "card": {
        "header": {
          "title": "AI Mitigation Plan",
          "subtitle": "Bulk Password Reset",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/lock_reset/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I identified 50 accounts belonging to a leaked database dump. Recommend immediate reset for the <b>Sales Org</b>."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Reset 50 Accounts",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/reset"
                        }
                      }
                    },
                    {
                      "text": "Wait for Helpdesk",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/wait"
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
