"""
ChatOps Card: brute_force_alert
Generated from brute_force_alert.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "brute-force-opt",
      "card": {
        "header": {
          "title": "Critical Security Alert",
          "subtitle": "Brute Force Attempt Detected",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/error/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "decoratedText": {
                  "topLabel": "Source IP",
                  "text": "192.168.1.105",
                  "startIcon": {
                    "knownIcon": "STAR"
                  }
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "View in Chronicle",
                      "onClick": {
                        "openLink": {
                          "url": "https://chronicle.security/"
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
