"""
ChatOps Card: ai_threat_intel_sharing
Generated from ai_threat_intel_sharing.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-share",
      "card": {
        "header": {
          "title": "AI Intel Sharing",
          "subtitle": "External IOC Submission",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/share/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I have extracted 5 unique IOCs from this incident. Should I share these anonymously with our industry <b>ISAC</b>?"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Share Anonymously",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/share"
                        }
                      }
                    },
                    {
                      "text": "Keep Internal",
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
