#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "bulk-delete", "card": {
    "header": { "title": "Data Loss Prevention", "subtitle": "Mass File Deletion Detected", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/delete_forever/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "Event", "text": "542 files deleted from OneDrive", "bottomLabel": "Target: /Archive/2023_Records"}},
      {"buttonList": {"buttons": [{"text": "Intentional", "onClick": {"openLink": {"url": "https://example.com/ok"}}}, {"text": "🚨 STOP & ROLLBACK", "onClick": {"openLink": {"url": "https://example.com/rollback"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
