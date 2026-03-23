"""
ChatOps Card: ai_sensitive_log_access
Generated from ai_sensitive_log_access.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-logs",
      "card": {
        "header": {
          "title": "AI Data Request",
          "subtitle": "Privileged Logs Required",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/policy/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "To continue investigating the insider threat, I need temporary access to <b>HR Personal Data</b> logs. This is outside my default scope."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Grant (1 Hour)", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Reject Request", "onClick": { "openLink": { "url": deny_url } } }
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
