#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{
    "cardId": "brute-force-opt",
    "card": {
      "header": { "title": "Critical Security Alert", "subtitle": "Brute Force Attempt Detected", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/error/default/48px.svg", "imageType": "CIRCLE" },
      "sections": [{ "widgets": [
        { "decoratedText": { "topLabel": "Source IP", "text": "192.168.1.105", "startIcon": { "knownIcon": "STAR" } } },
        { "buttonList": { "buttons": [ { "text": "View in Chronicle", "onClick": { "openLink": { "url": "https://chronicle.security/" } } } ]}}
      ]}]
    }
  }]
}' "$WEBHOOK_URL"
