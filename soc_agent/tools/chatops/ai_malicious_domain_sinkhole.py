"""
ChatOps Card: ai_malicious_domain_sinkhole
Generated from ai_malicious_domain_sinkhole.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-sink",
      "card": {
        "header": {
          "title": "AI DNS Defense",
          "subtitle": "Domain Sinkhole Request",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/location_off/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I have identified a new C2 domain: <b>evil-cloud-storage.net</b>. Requesting a global DNS sinkhole across the organization."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Sinkhole Domain",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/sink"
                        }
                      }
                    },
                    {
                      "text": "Review IOC",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/view"
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
