#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-audit", "card": {
    "header": { "title": "AI Config Audit", "subtitle": "Misconfiguration Found", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/security/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "Security Group <b>SG-992</b> allows SSH from 0.0.0.0/0. I recommend restricting this to our Corporate VPN IP."}},
      {"buttonList": {"buttons": [{"text": "Auto-Remediate", "onClick": {"openLink": {"url": "https://example.com/fix"}}}, {"text": "Ignore Project", "onClick": {"openLink": {"url": "https://example.com/ignore"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
