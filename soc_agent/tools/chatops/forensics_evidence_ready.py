"""
ChatOps Card: forensics_evidence_ready
Generated from forensics_evidence_ready.sh
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "forensics-zip",
      "card": {
        "header": {
          "title": "Forensics Complete",
          "subtitle": "Evidence Packet Collected",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/folder_zip/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "decoratedText": {
                  "topLabel": "Case ID",
                  "text": "INC-88219",
                  "bottomLabel": "Contents: Memory Dump, Event Logs"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Download Evidence",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/get-zip"
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
