#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "forensics-zip", "card": {
    "header": { "title": "Forensics Complete", "subtitle": "Evidence Packet Collected", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/folder_zip/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "Case ID", "text": "INC-88219", "bottomLabel": "Contents: Memory Dump, Event Logs"}},
      {"buttonList": {"buttons": [{"text": "Download Evidence", "onClick": {"openLink": {"url": "https://example.com/get-zip"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
