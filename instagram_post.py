import os

def get_caption():
    # 1. Try to get the caption sent from Telegram (via GitHub Env Var)
    telegram_caption = os.getenv('INSTAGRAM_CAPTION')

    # 2. If there is a telegram caption (it's not None and not empty), use it.
    if telegram_caption and telegram_caption.strip():
        return telegram_caption
    
    # 3. Otherwise (if running on schedule), use your default daily logic
    return "Here is my daily scheduled content! #daily #content"

# --- Your Main Code Starts Here ---

final_caption = get_caption()
print(f"Starting upload with caption: {final_caption}")

# Use 'final_caption' in your upload function below
# e.g. client.video_upload(path, caption=final_caption)
