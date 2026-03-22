#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-login-geo", "card": {
    "header": { "title": "AI Identity Monitor", "subtitle": "Suspicious VPN Egress", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/public/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "Account <b>Admin-X</b> just logged in from a known 'Tor' egress point. This is highly unusual for their persona."}},
      {"buttonList": {"buttons": [{"text": "Kill Session", "onClick": {"openLink": {"url": "https://example.com/end"}}}, {"text": "Start Monitor", "onClick": {"openLink": {"url": "https://example.com/watch"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
