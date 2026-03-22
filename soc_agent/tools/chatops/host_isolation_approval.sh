#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "host-iso", "card": {
    "header": { "title": "Containment Required", "subtitle": "Infection Confirmed", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/block/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "Host", "text": "DESKTOP-8291 (Finance-VLAN)", "bottomLabel": "Status: Active C2 identified"}},
      {"buttonList": {"buttons": [{"text": "🚫 Isolate Host Now", "onClick": {"openLink": {"url": "https://example.com/isolate"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
