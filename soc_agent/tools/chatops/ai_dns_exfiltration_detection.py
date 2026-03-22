"""
ChatOps Card: ai_dns_exfiltration_detection
Generated from ai_dns_exfiltration_detection.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-dns-exfil",
      "card": {
        "header": {
          "title": "AI Network Guardian",
          "subtitle": "DNS Tunneling Detected",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/dns/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "Detected high-frequency TXT record queries to <b>xyz.top-secret.io</b> from the backup server. This matches exfiltration fingerprints."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Block TLD",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/block"
                        }
                      }
                    },
                    {
                      "text": "False Positive",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/fp"
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
