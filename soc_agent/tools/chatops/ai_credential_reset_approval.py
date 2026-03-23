"""
ChatOps Card: ai_credential_reset_approval
Generated from ai_credential_reset_approval.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-pwd",
      "card": {
        "header": {
          "title": "AI Mitigation Plan",
          "subtitle": "Bulk Password Reset",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/lock_reset/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I identified 50 accounts belonging to a leaked database dump. Recommend immediate reset for the <b>Sales Org</b>."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Reset 50 Accounts", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Wait for Helpdesk", "onClick": { "openLink": { "url": deny_url } } }
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
