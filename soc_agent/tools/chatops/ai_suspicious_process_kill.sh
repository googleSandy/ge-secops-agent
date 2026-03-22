#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-kill", "card": {
    "header": { "title": "AI Active Defense", "subtitle": "Process Termination Request", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/potted_plant/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "Detected <b>powershell.exe</b> running an encoded script with high entropy on Admin-Workstation. Should I kill the process tree?"}},
      {"buttonList": {"buttons": [{"text": "Kill Process", "onClick": {"openLink": {"url": "https://example.com/kill"}}}, {"text": "Ignore", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
