import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace these with your actual details
TELEGRAM_BOT_TOKEN = '5477889304:AAGIrBexQdhdzlXWWoyrOVcjNdPKLh7WP_o'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_OWNER = 'Mythesis002'
GITHUB_REPO = 'test-telegram-msg'
WORKFLOW_FILENAME = 'main.yml'
PUBLIC_URL = 'https://test-telegram-msg-production.up.railway.app/'
# ---------------------

def log(message):
    """Helper to print logs immediately."""
    print(message, flush=True)

def trigger_github_action(text):
    if not GITHUB_OWNER or not GITHUB_REPO or not GITHUB_TOKEN:
        log("❌ Error: GitHub Configuration is missing.")
        return

    # --- DEBUGGING: PRINT TOKEN START ---
    # This helps us see if Railway is using the new token or the old one.
    token_start = GITHUB_TOKEN[:4] if GITHUB_TOKEN else "None"
    log(f"🔑 Using Token starting with: {token_start}...") 
    # ------------------------------------

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/main.yml/dispatches"
    headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
    }

    data = {"ref": "main", "inputs": {"telegram_msg": text}}
    
    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        log(f"✅ GitHub Triggered Successfully! Message: {text}")
    except Exception as e:
        log(f"❌ Error Triggering GitHub: {e}")
        if hasattr(e, 'response') and e.response is not None:
            log(f"GitHub Response: {e.response.text}")
def index():
    """Home page checks status."""
    log("Someone accessed the Home Page")
    
    missing = []
    if not TELEGRAM_BOT_TOKEN: missing.append("TELEGRAM_BOT_TOKEN")
    if not GITHUB_TOKEN: missing.append("GITHUB_TOKEN")
    if not PUBLIC_URL: missing.append("PUBLIC_URL")

    if missing:
        return f"❌ Error: Missing Variables: {', '.join(missing)}", 200

    webhook_url = f"{PUBLIC_URL}/webhook"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    
    try:
        # We re-set the webhook every time you visit home, just to be safe
        response = requests.post(telegram_url, json={"url": webhook_url})
        return f"Bot is Running! <br>Webhook response: {response.text}"
    except Exception as e:
        return f"Bot Running, but Webhook Failed: {e}"

@app.route('/webhook', methods=['POST'])
def receive_telegram_msg():
    """Main endpoint for Telegram messages."""
    try:
        # 1. Print Raw Data to prove connection
        raw_data = request.get_json()
        log(f"📥 RAW DATA RECEIVED: {json.dumps(raw_data)}")
        
        # 2. Check for message
        if raw_data and "message" in raw_data:
            text = raw_data["message"].get("text")
            if text:
                log(f"📩 Found Message Text: {text}")
                trigger_github_action(text)
            else:
                log("⚠️ Message received, but no text found (maybe a sticker or image?)")
        else:
            log("⚠️ Update received, but it is not a standard message.")
            
        return "OK", 200
    except Exception as e:
        log(f"❌ CRITICAL ERROR in webhook: {e}")
        return "Error", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
