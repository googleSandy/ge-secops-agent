"""
ChatOps Card: ai_forensic_image_approval
Generated from ai_forensic_image_approval.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-image",
      "card": {
        "header": {
          "title": "AI Forensics",
          "subtitle": "Memory Dump Request",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/memory/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I suspect memory-only malware on <b>SQL-PROD-01</b>. Requesting permission to take a full memory volatile image (may impact performance)."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Capture Image",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/dump"
                        }
                      }
                    },
                    {
                      "text": "Cancel",
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
