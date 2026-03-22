"""
ChatOps Card: temp_admin_request
Generated from temp_admin_request.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "temp-admin",
      "card": {
        "header": {
          "title": "Privilege Access",
          "subtitle": "PIM Request Elevation",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/admin_panel_settings/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "decoratedText": {
                  "topLabel": "Analyst",
                  "text": "Analyst-Smith",
                  "bottomLabel": "Duration: 60 mins"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Approve",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/ok"
                        }
                      }
                    },
                    {
                      "text": "Deny",
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
