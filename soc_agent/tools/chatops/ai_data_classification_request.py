"""
ChatOps Card: ai_data_classification_request
Generated from ai_data_classification_request.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-data-class",
      "card": {
        "header": {
          "title": "AI Data Classifier",
          "subtitle": "Sensitive Content Flagged",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/list_alt/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I found a file <b>'Project-Phoenix.xlsx'</b> that contains what look like social security numbers. Tag as PII?"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Tag as SENSITIVE",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/tag"
                        }
                      }
                    },
                    {
                      "text": "Mark False Pos",
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
