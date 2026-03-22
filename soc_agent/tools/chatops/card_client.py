import requests
import os
from pathlib import Path
from dotenv import load_dotenv

def send_card(card_json: dict, webhook_url: str = None):
    """Sends a card to Google Chat via webhook."""
    if not webhook_url:
        load_dotenv(Path(__file__).parent.parent.parent.parent / ".env")
        webhook_url = os.environ.get("WEBHOOK_URL")
    
    if not webhook_url:
        raise ValueError("WEBHOOK_URL not found in environment or arguments")
    
    response = requests.post(
        webhook_url,
        json=card_json,
        headers={"Content-Type": "application/json; charset=UTF-8"}
    )
    response.raise_for_status()
    return response.json()
