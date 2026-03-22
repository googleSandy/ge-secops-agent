#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-stale", "card": {
    "header": { "title": "AI Hygiene Bot", "subtitle": "Stale Account Cleanup", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/person_off/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I found 12 accounts with no logins in >90 days. I recommend disabling them immediately to reduce attack surface."}},
      {"buttonList": {"buttons": [{"text": "Disable All (12)", "onClick": {"openLink": {"url": "https://example.com/kill"}}}, {"text": "Notify Owners", "onClick": {"openLink": {"url": "https://example.com/ask"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
