#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-image", "card": {
    "header": { "title": "AI Forensics", "subtitle": "Memory Dump Request", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/memory/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I suspect memory-only malware on <b>SQL-PROD-01</b>. Requesting permission to take a full memory volatile image (may impact performance)."}},
      {"buttonList": {"buttons": [{"text": "Capture Image", "onClick": {"openLink": {"url": "https://example.com/dump"}}}, {"text": "Cancel", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
