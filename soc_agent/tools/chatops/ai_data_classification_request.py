"""
ChatOps Card: ai_data_classification_request
Generated from ai_data_classification_request.sh
"""
from card_client import send_card, generate_action_url


def get_card(session_id: str = None, agent_engine_id: str = None, user_id: str = None):
    # Dynamic URLs
    approve_url = generate_action_url("Approve", session_id, agent_engine_id, user_id=user_id)
    deny_url = generate_action_url("Deny", session_id, agent_engine_id, user_id=user_id)
    return {
  "cardsV2": [
    {
      "cardId": "ai-data-class",
      "card": {
        "header": {
          "title": "AI Data Classifier",
          "subtitle": "Sensitive Content Flagged",
          "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/list_alt/default/48px.svg",
          "imageType": "CIRCLE"
        },
        "sections": [
          {
            "widgets": [
              {
                "textParagraph": {
                  "text": "I found a file <b>'Project-Phoenix.xlsx'</b> that contains what look like social security numbers. Tag as PII?"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    { "text": "Tag as SENSITIVE", "onClick": { "openLink": { "url": approve_url } } },
                    { "text": "Mark False Pos", "onClick": { "openLink": { "url": deny_url } } }
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
