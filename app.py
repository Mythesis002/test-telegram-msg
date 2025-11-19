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

def trigger_github_workflow(message_text):
    """Sends a dispatch event to GitHub Actions."""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/{WORKFLOW_FILENAME}/dispatches"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "ref": "main",  # Ensure this matches your default branch
        "inputs": {
            "telegram_msg": message_text
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise an error for bad status codes
        print(f"Successfully triggered GitHub Action! Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger GitHub Action: {e}")
        if e.response is not None:
             print(f"GitHub Response: {e.response.text}")

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram."""
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Check if the update contains a message with text
    message = data.get('message', {})
    text = message.get('text')

    if text:
        print(f"Received message: {text}")
        trigger_github_workflow(text)

    return "OK", 200

def set_webhook():
    """Sets the Telegram webhook URL."""
    # NOTE: Replace with your PUBLIC URL (e.g., https://your-app.onrender.com/webhook)
    # Localhost will NOT work for Telegram.
    webhook_url = "https://YOUR_PUBLIC_URL.com/webhook" 
    
    try:
        response = requests.post(f"{TELEGRAM_API_URL}/setWebhook", json={"url": webhook_url})
        print(f"Webhook set response: {response.text}")
    except Exception as e:
        print(f"Error setting webhook: {e}")

if __name__ == '__main__':
    # Optional: Set webhook on startup (useful for development/first deploy)
    # set_webhook() 
    
    port = int(os.environ.get('PORT', 3000))
    print(f"Server is running on port {port}")
    app.run(host='0.0.0.0', port=port)
