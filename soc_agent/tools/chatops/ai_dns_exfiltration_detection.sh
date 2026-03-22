#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-dns-exfil", "card": {
    "header": { "title": "AI Network Guardian", "subtitle": "DNS Tunneling Detected", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/dns/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "Detected high-frequency TXT record queries to <b>xyz.top-secret.io</b> from the backup server. This matches exfiltration fingerprints."}},
      {"buttonList": {"buttons": [{"text": "Block TLD", "onClick": {"openLink": {"url": "https://example.com/block"}}}, {"text": "False Positive", "onClick": {"openLink": {"url": "https://example.com/fp"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
