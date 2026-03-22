#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-close", "card": {
    "header": { "title": "AI Case Manager", "subtitle": "Incident Closure Request", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/task_alt/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "All remediation steps for <b>INC-445</b> are complete. IOCs blocked, host reimaged, user notified. Close the ticket?"}},
      {"buttonList": {"buttons": [{"text": "Close Ticket", "onClick": {"openLink": {"url": "https://example.com/close"}}}, {"text": "Needs More Work", "onClick": {"openLink": {"url": "https://example.com/no"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
