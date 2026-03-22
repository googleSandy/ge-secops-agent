"""
ChatOps Card: ai_draft_comms_review
Generated from ai_draft_comms_review.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-comms",
      "card": {
        "header": {
          "title": "AI Comms Draft",
          "subtitle": "Customer Notification Email",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/edit_note/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I have drafted a breach notification for the Engineering org. Please review for tone and accuracy."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Review Draft",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/draft"
                        }
                      }
                    },
                    {
                      "text": "Send As-Is",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/send"
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
