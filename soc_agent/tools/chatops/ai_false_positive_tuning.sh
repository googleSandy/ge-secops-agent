#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-tune", "card": {
    "header": { "title": "AI Rule Optimization", "subtitle": "Rule Noise Reduction", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/tune/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "The rule <b>Brute Force (Generic)</b> has a 95% FP rate this week. I have drafted an exception for the Jenkins IP."}},
      {"buttonList": {"buttons": [{"text": "Apply Tuning", "onClick": {"openLink": {"url": "https://example.com/ok"}}}, {"text": "Keep Noisy", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
