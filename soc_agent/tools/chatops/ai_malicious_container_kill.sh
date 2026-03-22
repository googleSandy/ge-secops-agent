#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-k8s-kill", "card": {
    "header": { "title": "AI Runtime Defense", "subtitle": "Container Compromise Detected", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/view_in_ar/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "Pod <b>'auth-api-88x'</b> is consuming 100% CPU on Cryptominer signatures. Should I kill and redeploy from safe image?"}},
      {"buttonList": {"buttons": [{"text": "Kill & Redeploy", "onClick": {"openLink": {"url": "https://example.com/redeploy"}}}, {"text": "Debug Console", "onClick": {"openLink": {"url": "https://example.com/debug"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
