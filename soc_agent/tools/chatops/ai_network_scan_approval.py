"""
ChatOps Card: ai_network_scan_approval
Generated from ai_network_scan_approval.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-scan",
      "card": {
        "header": {
          "title": "AI Investigation Step",
          "subtitle": "Network Probe Request",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/radar/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I suspect lateral movement. I want to run a non-intrusive scan of the <b>10.0.5.0/24 (Production)</b> subnet to identify active listeners."
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Approve Scan", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Prohibit Scan", "onClick": { "openLink": { "url": deny_url } } }
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
