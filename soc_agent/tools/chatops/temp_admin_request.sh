#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "temp-admin", "card": {
    "header": { "title": "Privilege Access", "subtitle": "PIM Request Elevation", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/admin_panel_settings/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "Analyst", "text": "Analyst-Smith", "bottomLabel": "Duration: 60 mins"}},
      {"buttonList": {"buttons": [{"text": "Approve", "onClick": {"openLink": {"url": "https://example.com/ok"}}}, {"text": "Deny", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
