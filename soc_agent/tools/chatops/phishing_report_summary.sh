#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "phishing-sum", "card": {
    "header": { "title": "Phishing Triage", "subtitle": "Multiple Reports for Campaign", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/mail/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "Subject", "text": "Urgent: Review your salary", "bottomLabel": "Reporting users: 12"}},
      {"decoratedText": {"topLabel": "URL Status", "text": "Credential Harvester (Known)", "startIcon": {"knownIcon": "CONFIRMATION_NUMBER_ICON"}}},
      {"buttonList": {"buttons": [{"text": "Purge from Inbox", "onClick": {"openLink": {"url": "https://example.com/purge"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
