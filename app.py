import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace these with your actual details
TELEGRAM_BOT_TOKEN = '5477889304:AAGIrBexQdhdzlXWWoyrOVcjNdPKLh7WP_o'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# GitHub Configuration
GITHUB_TOKEN = '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'
GITHUB_OWNER = 'Mythesis002'
GITHUB_REPO = 'test-telegram-msg'
WORKFLOW_FILENAME = 'main.yml'
# ---------------------

def trigger_github_action(text):
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/main.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": "main", "inputs": {"telegram_msg": text}}
    
    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        print(f"✅ GitHub Triggered: {text}")
    except Exception as e:
        print(f"❌ Error Triggering GitHub: {e}")

@app.route('/', methods=['GET'])
def index():
    """Accessing the root URL manually sets the webhook."""
    if not PUBLIC_URL or not TELEGRAM_BOT_TOKEN:
        return "Missing Variables (PUBLIC_URL or TELEGRAM_BOT_TOKEN)", 500
    
    # Set Webhook
    webhook_url = f"{PUBLIC_URL}/webhook"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    
    try:
        response = requests.post(telegram_url, json={"url": webhook_url})
        return f"Bot is Running! <br>Webhook Response: {response.text}"
    except Exception as e:
        return f"Bot Running, but Webhook Failed: {e}"

@app.route('/webhook', methods=['POST'])
def receive_telegram_msg():
    update = request.get_json()
    if update and "message" in update:
        text = update["message"].get("text")
        if text:
            print(f"📩 Message: {text}")
            trigger_github_action(text)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
