#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-priv-audit", "card": {
    "header": { "title": "AI IAM Auditor", "subtitle": "Excessive Permissions Found", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/manage_accounts/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "User <b>b.wayne</b> has Domain Admin rights but hasn’t used them in 6 months. I recommend downgrading to Standard User."}},
      {"buttonList": {"buttons": [{"text": "Strip Extra Privs", "onClick": {"openLink": {"url": "https://example.com/strip"}}}, {"text": "Keep Access", "onClick": {"openLink": {"url": "https://example.com/keep"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
