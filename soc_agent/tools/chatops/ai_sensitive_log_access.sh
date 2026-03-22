#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-logs", "card": {
    "header": { "title": "AI Data Request", "subtitle": "Privileged Logs Required", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/policy/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "To continue investigating the insider threat, I need temporary access to <b>HR Personal Data</b> logs. This is outside my default scope."}},
      {"buttonList": {"buttons": [{"text": "Grant (1 Hour)", "onClick": {"openLink": {"url": "https://example.com/grant"}}}, {"text": "Reject Request", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
