#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-fw", "card": {
    "header": { "title": "AI Agent Request", "subtitle": "Temporary Firewall Bypass", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/shield_with_house/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I need to egress forensic logs from <b>Isolated-VLAN-9</b> to my analysis bucket. Requesting a 10-minute bypass for port 443."}},
      {"buttonList": {"buttons": [{"text": "Open Port (10m)", "onClick": {"openLink": {"url": "https://example.com/open"}}}, {"text": "Deny", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
