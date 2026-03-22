"""
ChatOps Card: ai_privileged_session_recording
Generated from ai_privileged_session_recording.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ai-record",
      "card": {
        "header": {
          "title": "AI Session Audit",
          "subtitle": "High-Risk Session Found",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/videocam/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "A privileged session was just opened by <b>Contractor-A</b> on a sensitive DB. I recommend turning on full session recording."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Start Recording",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/rec"
                        }
                      }
                    },
                    {
                      "text": "Analyst Monitor",
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
