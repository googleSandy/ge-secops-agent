
source "$(dirname "$0")/.env"

curl -X POST \
  -H "Content-Type: application/json; charset=UTF-8" \
  -d '{
    "cardsV2": [{
      "cardId": "secops-alert-001",
      "card": {
        "header": {
          "title": "Critical Security Alert",
          "subtitle": "Project: secops-demo-env",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/error/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "header": "Incident Details",
            "widgets": [
              {
                "decoratedText": {
                  "topLabel": "Detection Type",
                  "text": "Brute Force Attempt",
                  "startIcon": { "knownIcon": "STAR" }
                }
              },
              {
                "decoratedText": {
                  "topLabel": "Source IP",
                  "text": "192.168.1.105",
                  "bottomLabel": "Location: Unknown",
                  "startIcon": { "knownIcon": "BOOKMARK" }
                }
              }
            ]
          },
          {
            "widgets": [
              {
                "buttonList": {
                  "buttons": [
                    {
                      "text": "View in Chronicle",
                      "onClick": {
                        "openLink": {
                          "url": "https://chronicle.security/investigation/secops-demo-env"
                        }
                      }
                    },
                    {
                      "text": "Open Runbook",
                      "onClick": {
                        "openLink": {
                          "url": "https://example.com/soar/playbook-123"
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
    }]
  }' \
  "$WEBHOOK_URL"
