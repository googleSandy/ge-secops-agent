#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-summary", "card": {
    "header": { "title": "AI Agent Reasoning", "subtitle": "Incident #992 Analysis", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/psychology/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "<b>Summary:</b> I have linked three failed logins to a later successful VPN entry. I believe this is valid Credential Stuffing."}},
      {"buttonList": {"buttons": [{"text": "Correct, proceed", "onClick": {"openLink": {"url": "https://example.com/ok"}}}, {"text": "Mistaken, close", "onClick": {"openLink": {"url": "https://example.com/close"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
