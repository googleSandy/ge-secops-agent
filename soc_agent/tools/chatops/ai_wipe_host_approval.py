"""
ChatOps Card: ai_wipe_host_approval
Generated from ai_wipe_host_approval.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-wipe",
      "card": {
        "header": {
          "title": "AI Remediation Plan",
          "subtitle": "Host Reimage Request",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/desktop_access_disabled/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "AI has detected Rootkit behavior on <b>WS-099</b>. Standard cleaning failed. Requesting full disk wipe and reimage."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Authorized",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/wipe"
                        }
                      }
                    },
                    {
                      "text": "Deny / Manual Fix",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/manual"
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
