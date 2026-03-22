#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-data-class", "card": {
    "header": { "title": "AI Data Classifier", "subtitle": "Sensitive Content Flagged", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/list_alt/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I found a file <b>'Project-Phoenix.xlsx'</b> that contains what look like social security numbers. Tag as PII?"}},
      {"buttonList": {"buttons": [{"text": "Tag as SENSITIVE", "onClick": {"openLink": {"url": "https://example.com/tag"}}}, {"text": "Mark False Pos", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
