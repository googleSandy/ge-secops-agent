#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ioc-enrich", "card": {
    "header": { "title": "IOC Enrichment", "subtitle": "Intelligence for IP 1.2.3.4", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/hub/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"decoratedText": {"topLabel": "CrowdStrike", "text": "Tagged: Fancy Bear / APT28"}},
      {"decoratedText": {"topLabel": "VirusTotal", "text": "45/70 detections"}},
      {"buttonList": {"buttons": [{"text": "Investigate History", "onClick": {"openLink": {"url": "https://example.com/history"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
