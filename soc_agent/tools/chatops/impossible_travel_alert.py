"""
ChatOps Card: impossible_travel_alert
Modernized Version
"""
from card_client import send_card

def get_card():
    return {
    "cardsV2": [
      {
        "cardId": "impossible-travel",
        "card": {
          "header": {
            "title": "Impossible Travel Alert",
            "subtitle": "Multiple Logins from Distant Locations",
            "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/flight_land/default/48px.svg",
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
                              "topLabel": "User Account",
                              "text": "john.doe@example.com",
                              "startIcon": { "materialIcon": { "name": "person" } }
                            }
                          }
                        ]
                      },
                      {
                        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                        "widgets": [
                          {
                            "decoratedText": {
                              "topLabel": "Severity",
                              "text": "<b>High</b>",
                              "startIcon": { "materialIcon": { "name": "priority_high" } }
                            }
                          }
                        ]
                      }
                    ]
                  }
                },
                {
                  "columns": {
                    "columnItems": [
                      {
                        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                        "widgets": [
                          {
                            "decoratedText": {
                              "topLabel": "Location 1",
                              "text": "New York, USA",
                              "startIcon": { "materialIcon": { "name": "place" } }
                            }
                          }
                        ]
                      },
                      {
                        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE",
                        "widgets": [
                          {
                            "decoratedText": {
                              "topLabel": "Location 2",
                              "text": "London, UK",
                              "startIcon": { "materialIcon": { "name": "place" } }
                            }
                          }
                        ]
                      }
                    ]
                  }
                },
                {
                    "textParagraph": {
                        "text": "Logins were attempted within 15 minutes. This usually indicates account sharing or compromise."
                    }
                },
                {
                  "buttonList": {
                    "buttons": [
                      {
                        "text": "Require MFA",
                        "color": { "red": 0, "green": 0.5, "blue": 1 },
                        "onClick": { "openLink": { "url": "https://example.com/mfa" } }
                      },
                      {
                        "text": "Reset Password",
                        "color": { "red": 0.8, "green": 0, "blue": 0 },
                        "onClick": { "openLink": { "url": "https://example.com/reset" } }
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
