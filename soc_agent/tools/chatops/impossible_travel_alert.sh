#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{
    "cardId": "impossible-travel-opt",
    "card": {
      "header": { "title": "Security Verification", "subtitle": "Impossible Travel Detected", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/travel_explore/default/48px.svg", "imageType": "CIRCLE" },
      "sections": [{ "widgets": [
        { "decoratedText": { "topLabel": "Current Login", "text": "London, UK (IP: 85.112.x.x)", "startIcon": { "knownIcon": "FLIGHT_TAKEOFF" } } },
        { "buttonList": { "buttons": [ { "text": "Yes, it was me", "onClick": { "openLink": { "url": "https://example.com/approve" } } }, { "text": "No, investigate", "onClick": { "openLink": { "url": "https://example.com/report" } } } ]}}
      ]}]
    }
  }]
}' "$WEBHOOK_URL"
