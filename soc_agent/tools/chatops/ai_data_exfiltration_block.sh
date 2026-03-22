#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-exfil", "card": {
    "header": { "title": "AI DLP Alert", "subtitle": "Large Outbound Transfer", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/upload_file/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "User John Doe is uploading 14GB to <b>mega.nz</b>. This is atypical for their role. Should I shard the network connection?"}},
      {"buttonList": {"buttons": [{"text": "Terminate Transfer", "onClick": {"openLink": {"url": "https://example.com/kill"}}}, {"text": "Acknowledge Only", "onClick": {"openLink": {"url": "https://example.com/ok"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
