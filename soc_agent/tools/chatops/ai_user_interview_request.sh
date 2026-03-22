#!/bin/bash
source "$(dirname "$0")/.env"
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{
  "cardsV2": [{"cardId": "ai-interview", "card": {
    "header": { "title": "AI Agent Action", "subtitle": "User Interview Permission", "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/chat_paste_go/default/48px.svg", "imageType": "CIRCLE" },
    "sections": [{ "widgets": [
      {"textParagraph": {"text": "I want to DM <b>User: JaneDoe</b> to verify their recent sign-in from a new country. Should I proceed with the automated interview?"}},
      {"buttonList": {"buttons": [{"text": "Start Interview", "onClick": {"openLink": {"url": "https://example.com/chat"}}}, {"text": "Analyst will handle", "onClick": {"openLink": {"url": "https://example.com/manual"}}}]}}
    ]}]
  }}]
}' "$WEBHOOK_URL"
