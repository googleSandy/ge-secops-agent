"""
ChatOps Card: host_isolation_approval
Modernized Version
"""
from card_client import send_card

def get_card():
    return {
    "cardsV2": [
      {
        "cardId": "host-iso",
        "card": {
          "header": {
            "title": "Containment Required",
            "subtitle": "Active Infection Confirmed",
            "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/block/default/48px.svg",
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
                              "topLabel": "Host Name",
                              "text": "DESKTOP-8291",
                              "startIcon": { "materialIcon": { "name": "computer" } }
                            }
                          }
                        ]
                      },
                      {
                        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                        "widgets": [
                          {
                            "decoratedText": {
                              "topLabel": "Network segment",
                              "text": "Finance-VLAN",
                              "startIcon": { "materialIcon": { "name": "hub" } }
                            }
                          }
                        ]
                      }
                    ]
                  }
                },
                {
                    "decoratedText": {
                        "topLabel": "Detection Status",
                        "text": "<font color=\"#ff0000\">Active C2 identified</font>",
                        "bottomLabel": "Confirmed via SIEM/EDR logs",
                        "startIcon": { "materialIcon": { "name": "security" } }
                    }
                },
                {
                  "buttonList": {
                    "buttons": [
                      {
                        "text": "Isolate Host Now",
                        "color": { "red": 0.8, "green": 0, "blue": 0 },
                        "onClick": { "openLink": { "url": "https://example.com/isolate" } }
                      },
                      {
                        "text": "Ignore (False Positive)",
                        "onClick": { "openLink": { "url": "https://example.com/ignore" } }
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
