#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-canary", "card": {
    "header": { "title": "AI Countermeasures", "subtitle": "Canary Token Deployment", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/featured_video/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I am tracking an active explorer in the network. I want to deploy 10 <b>Honey-Files</b> (AWS Keys, Passwords.txt) to track their movement."}},
      {"buttonList": {"buttons": [{"text": "Deploy Canaries", "onClick": {"openLink": {"url": "https://example.com/drop"}}}, {"text": "Not now", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
