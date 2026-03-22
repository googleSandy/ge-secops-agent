"""
ChatOps Card: ai_compliance_violation_alert
Generated from ai_compliance_violation_alert.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-compliance",
      "card": {
        "header": {
          "title": "AI Compliance Bot",
          "subtitle": "Unencrypted Asset Found",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/gavel/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "S3 Bucket <b>'finance-reports-2024'</b> is public and unencrypted. This violates our SOC2 framework. Auto-remediate now?"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Encrypt & Private",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/fix"
                        }
                      }
                    },
                    {
                      "text": "Mark Exception",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/exc"
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
