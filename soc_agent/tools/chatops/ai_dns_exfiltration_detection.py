"""
ChatOps Card: ai_dns_exfiltration_detection
Generated from ai_dns_exfiltration_detection.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-dns-exfil",
      "card": {
        "header": {
          "title": "AI Network Guardian",
          "subtitle": "DNS Tunneling Detected",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/dns/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "Detected high-frequency TXT record queries to <b>xyz.top-secret.io</b> from the backup server. This matches exfiltration fingerprints."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Block TLD", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "False Positive", "onClick": { "openLink": { "url": deny_url } } }
                  ]
                }
              }
            ]
          }
        ]
      }
    }
  ]
}

if __name__ == "__main__":
    card = get_card(session_id="test-session", agent_engine_id="test-agent", user_id="test-user")
    send_card(card)
