"""
ChatOps Card: phishing_report_summary
Modernized Version
"""
from card_client import send_card

def get_card():
    return {
    "cardsV2": [{
      "cardId": "phishing-report",
      "card": {
        "header": {
          "title": "Phishing Report Summary",
          "subtitle": "Multiple User Reports",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/phishing/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "columns": {
                  "columnItems": [
                    {
                      "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                      "widgets": [
                        {
                          "decoratedText": {
                            "topLabel": "Target",
                            "text": "Finance / HR",
                            "startIcon": { "materialIcon": { "name": "groups" } }
                          }
                        }
                      ]
                    },
                    {
                      "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                      "widgets": [
                        {
                          "decoratedText": {
                            "topLabel": "Sentiment",
                            "text": "Suspicious",
                            "startIcon": { "materialIcon": { "name": "mood_bad" } }
                          }
                        }
                      ]
                    }
                  ]
                }
              },
              {
                "textParagraph": {
                    "text": "Analysis indicates a phishing campaign targeting executives. Use the buttons below to investigate additional details."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Check VirusTotal",
                      "color": { "red": 0, "green": 0.5, "blue": 1 },
                      "onClick": { "openLink": { "url": "https://virustotal.com" } }
                    },
                    {
                      "text": "Delete emails",
                      "color": { "red": 0.8, "green": 0, "blue": 0 },
                      "onClick": { "openLink": { "url": "https://example.com/del" } }
                    }
                  ]
                }
              }
            ]
          }
        ]
      }
    }]
  }

if __name__ == "__main__":
    send_card(get_card())
