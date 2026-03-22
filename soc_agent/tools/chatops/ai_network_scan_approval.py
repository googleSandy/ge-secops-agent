"""
ChatOps Card: ai_network_scan_approval
Generated from ai_network_scan_approval.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-scan",
      "card": {
        "header": {
          "title": "AI Investigation Step",
          "subtitle": "Network Probe Request",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/radar/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I suspect lateral movement. I want to run a non-intrusive scan of the <b>10.0.5.0/24 (Production)</b> subnet to identify active listeners."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Approve Scan",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/scan"
                        }
                      }
                    },
                    {
                      "text": "Prohibit Scan",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/block"
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
