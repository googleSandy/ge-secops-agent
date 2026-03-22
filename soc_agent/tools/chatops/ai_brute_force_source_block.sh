#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-fw-block", "card": {
    "header": { "title": "AI Auto-Defender", "subtitle": "Persistent Bot Identification", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/security_update_warning/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "IP <b>185.x.x.x</b> has failed 5,000 logins across multiple tenants. This is a clear global bot. Apply permanent blacklist?"}},
      {"buttonList": {"buttons": [{"text": "Global Blacklist", "onClick": {"openLink": {"url": "https://example.com/ban"}}}, {"text": "Ignore", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
