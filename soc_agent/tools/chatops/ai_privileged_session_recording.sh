#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-record", "card": {
    "header": { "title": "AI Session Audit", "subtitle": "High-Risk Session Found", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/videocam/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "A privileged session was just opened by <b>Contractor-A</b> on a sensitive DB. I recommend turning on full session recording."}},
      {"buttonList": {"buttons": [{"text": "Start Recording", "onClick": {"openLink": {"url": "https://example.com/rec"}}}, {"text": "Analyst Monitor", "onClick": {"openLink": {"url": "https://example.com/view"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
