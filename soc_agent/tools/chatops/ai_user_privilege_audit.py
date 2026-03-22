"""
ChatOps Card: ai_user_privilege_audit
Generated from ai_user_privilege_audit.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-priv-audit",
      "card": {
        "header": {
          "title": "AI IAM Auditor",
          "subtitle": "Excessive Permissions Found",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/manage_accounts/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "User <b>b.wayne</b> has Domain Admin rights but hasn\u2019t used them in 6 months. I recommend downgrading to Standard User."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Strip Extra Privs",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/strip"
                        }
                      }
                    },
                    {
                      "text": "Keep Access",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/keep"
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
