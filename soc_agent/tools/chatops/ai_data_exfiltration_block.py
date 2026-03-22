"""
ChatOps Card: ai_data_exfiltration_block
Generated from ai_data_exfiltration_block.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-exfil",
      "card": {
        "header": {
          "title": "AI DLP Alert",
          "subtitle": "Large Outbound Transfer",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/upload_file/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "User John Doe is uploading 14GB to <b>mega.nz</b>. This is atypical for their role. Should I shard the network connection?"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Terminate Transfer",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/kill"
                        }
                      }
                    },
                    {
                      "text": "Acknowledge Only",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/ok"
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
