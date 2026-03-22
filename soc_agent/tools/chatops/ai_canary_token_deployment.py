"""
ChatOps Card: ai_canary_token_deployment
Generated from ai_canary_token_deployment.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-canary",
      "card": {
        "header": {
          "title": "AI Countermeasures",
          "subtitle": "Canary Token Deployment",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/featured_video/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I am tracking an active explorer in the network. I want to deploy 10 <b>Honey-Files</b> (AWS Keys, Passwords.txt) to track their movement."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Deploy Canaries",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/drop"
                        }
                      }
                    },
                    {
                      "text": "Not now",
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
