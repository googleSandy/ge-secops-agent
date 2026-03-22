"""
ChatOps Card: ai_false_positive_tuning
Generated from ai_false_positive_tuning.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-tune",
      "card": {
        "header": {
          "title": "AI Rule Optimization",
          "subtitle": "Rule Noise Reduction",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/tune/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "The rule <b>Brute Force (Generic)</b> has a 95% FP rate this week. I have drafted an exception for the Jenkins IP."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Apply Tuning",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/ok"
                        }
                      }
                    },
                    {
                      "text": "Keep Noisy",
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
