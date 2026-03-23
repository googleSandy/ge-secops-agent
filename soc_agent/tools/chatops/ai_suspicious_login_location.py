"""
ChatOps Card: ai_suspicious_login_location
Generated from ai_suspicious_login_location.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-login-geo",
      "card": {
        "header": {
          "title": "AI Identity Monitor",
          "subtitle": "Suspicious VPN Egress",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/public/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "Account <b>Admin-X</b> just logged in from a known 'Tor' egress point. This is highly unusual for their persona."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Kill Session", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Start Monitor", "onClick": { "openLink": { "url": deny_url } } }
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
