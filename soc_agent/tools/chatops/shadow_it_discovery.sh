#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "shadow-it", "card": {
    "header": { "title": "Application Discovery", "subtitle": "New App Connected to GSuite", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/category/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "App Name", "text": "Trello-Clone-v2", "bottomLabel": "Permissions: Read/Write Drive"}},
      {"buttonList": {"buttons": [{"text": "Business Use", "onClick": {"openLink": {"url": "https://example.com/tag-business"}}}, {"text": "Personal Use", "onClick": {"openLink": {"url": "https://example.com/tag-personal"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
