#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-comms", "card": {
    "header": { "title": "AI Comms Draft", "subtitle": "Customer Notification Email", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/edit_note/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I have drafted a breach notification for the Engineering org. Please review for tone and accuracy."}},
      {"buttonList": {"buttons": [{"text": "Review Draft", "onClick": {"openLink": {"url": "https://example.com/draft"}}}, {"text": "Send As-Is", "onClick": {"openLink": {"url": "https://example.com/send"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
