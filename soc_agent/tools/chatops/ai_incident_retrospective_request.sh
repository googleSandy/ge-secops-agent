#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-postmortem", "card": {
    "header": { "title": "AI Retrospective", "subtitle": "Post-Mortem Draft Ready", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/history_edu/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I have compiled the timeline and root cause for <b>INC-2024-001</b>. Please review and publish the report."}},
      {"buttonList": {"buttons": [{"text": "Open Report Draft", "onClick": {"openLink": {"url": "https://example.com/report"}}}, {"text": "Archive Incident", "onClick": {"openLink": {"url": "https://example.com/archive"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
