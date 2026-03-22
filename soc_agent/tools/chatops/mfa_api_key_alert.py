"""
ChatOps Card: mfa_api_key_alert
Generated from mfa_api_key_alert.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "mfa-api-key-opt",
      "card": {
        "header": {
          "title": "MFA Verification",
          "subtitle": "New API Key Created",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/vpn_key/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "decoratedText": {
                  "topLabel": "User",
                  "text": "dandye@example.com",
                  "startIcon": {
                    "knownIcon": "PERSON"
                  }
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
                      "text": "Revoke",
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
