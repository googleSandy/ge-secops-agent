#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-play", "card": {
    "header": { "title": "AI SOAR Orchestrator", "subtitle": "Next Steps Recommendation", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/rebase/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I have completed initial triage. Based on incident signature, which playbook should I launch?"}},
      {"buttonList": {"buttons": [{"text": "Full Ransomware Response", "onClick": {"openLink": {"url": "https://example.com/r-book"}}}, {"text": "Standard Malware Triage", "onClick": {"openLink": {"url": "https://example.com/m-book"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
