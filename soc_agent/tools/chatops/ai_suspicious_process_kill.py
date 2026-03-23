"""
ChatOps Card: ai_suspicious_process_kill
Generated from ai_suspicious_process_kill.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-kill",
      "card": {
        "header": {
          "title": "AI Active Defense",
          "subtitle": "Process Termination Request",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/potted_plant/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "Detected <b>powershell.exe</b> running an encoded script with high entropy on Admin-Workstation. Should I kill the process tree?"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Kill Process", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Ignore", "onClick": { "openLink": { "url": deny_url } } }
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
