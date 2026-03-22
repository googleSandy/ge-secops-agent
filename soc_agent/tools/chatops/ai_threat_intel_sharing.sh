#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-share", "card": {
    "header": { "title": "AI Intel Sharing", "subtitle": "External IOC Submission", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/share/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I have extracted 5 unique IOCs from this incident. Should I share these anonymously with our industry <b>ISAC</b>?"}},
      {"buttonList": {"buttons": [{"text": "Share Anonymously", "onClick": {"openLink": {"url": "https://example.com/share"}}}, {"text": "Keep Internal", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
