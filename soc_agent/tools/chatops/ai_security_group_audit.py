"""
ChatOps Card: ai_security_group_audit
Generated from ai_security_group_audit.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-audit",
      "card": {
        "header": {
          "title": "AI Config Audit",
          "subtitle": "Misconfiguration Found",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/security/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "Security Group <b>SG-992</b> allows SSH from 0.0.0.0/0. I recommend restricting this to our Corporate VPN IP."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Auto-Remediate",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/fix"
                        }
                      }
                    },
                    {
                      "text": "Ignore Project",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/ignore"
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
