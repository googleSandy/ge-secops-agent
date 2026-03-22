#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-compliance", "card": {
    "header": { "title": "AI Compliance Bot", "subtitle": "Unencrypted Asset Found", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/gavel/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "S3 Bucket <b>'finance-reports-2024'</b> is public and unencrypted. This violates our SOC2 framework. Auto-remediate now?"}},
      {"buttonList": {"buttons": [{"text": "Encrypt & Private", "onClick": {"openLink": {"url": "https://example.com/fix"}}}, {"text": "Mark Exception", "onClick": {"openLink": {"url": "https://example.com/exc"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
