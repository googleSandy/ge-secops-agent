#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-sink", "card": {
    "header": { "title": "AI DNS Defense", "subtitle": "Domain Sinkhole Request", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/location_off/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I have identified a new C2 domain: <b>evil-cloud-storage.net</b>. Requesting a global DNS sinkhole across the organization."}},
      {"buttonList": {"buttons": [{"text": "Sinkhole Domain", "onClick": {"openLink": {"url": "https://example.com/sink"}}}, {"text": "Review IOC", "onClick": {"openLink": {"url": "https://example.com/view"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
