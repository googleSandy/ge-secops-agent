"""
ChatOps Card: ioc_enrichment_card
Modernized Version
"""
from card_client import send_card

def get_card():
    return {
  "cardsV2": [
    {
      "cardId": "ioc-enrich",
      "card": {
        "header": {
          "title": "IOC Enrichment",
          "subtitle": "Intelligence for IP 1.2.3.4",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/hub/default/48px.svg",
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
                            "topLabel": "CrowdStrike",
                            "text": "Fancy Bear / APT28",
                            "startIcon": { "materialIcon": { "name": "flag" } }
                          }
                        }
                      ]
                    },
                    {
                      "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                      "widgets": [
                        {
                          "decoratedText": {
                            "topLabel": "VirusTotal",
                            "text": "<font color=\"#ff0000\">45/70</font> Detections",
                            "startIcon": { "materialIcon": { "name": "security" } }
                          }
                        }
                      ]
                    }
                  ]
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "Investigate History",
                      "color": { "red": 0.1, "green": 0.5, "blue": 1.0 },
                      "onClick": { "openLink": { "url": "https://example.com/history" } }
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
    send_card(get_card())
