#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{
    "cardId": "mfa-api-key-opt",
    "card": {
      "header": { "title": "MFA Verification", "subtitle": "New API Key Created", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/vpn_key/default/48px.svg", "imageType": "CIRCLE" },
      "sections": [{ "widgets": [
        { "decoratedText": { "topLabel": "User", "text": "dandye@example.com", "startIcon": { "knownIcon": "PERSON" } } },
        { "buttonList": { "buttons": [ { "text": "Approve", "onClick": { "openLink": { "url": "https://example.com/ok" } } }, { "text": "Revoke", "onClick": { "openLink": { "url": "https://example.com/no" } } } ]}}
      ]}]
    }
  }]
}' "$WEBHOOK_URL"
