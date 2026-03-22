#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-hunt", "card": {
    "header": { "title": "AI Threat Hunting", "subtitle": "New Hypothesis Generated", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/travel_explore/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "Based on recent industry trends, I suspect our <b>SolarWinds</b> instances may have old orphaned credentials. Start a hunt?"}},
      {"buttonList": {"buttons": [{"text": "Launch Hunt", "onClick": {"openLink": {"url": "https://example.com/hunt"}}}, {"text": "Save for later", "onClick": {"openLink": {"url": "https://example.com/save"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
