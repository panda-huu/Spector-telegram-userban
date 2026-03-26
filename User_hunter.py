import requests
from telegram import Bot

async def get_user_id(bot_token, username):
    """Username → User ID converter"""
    bot = Bot(token=bot_token)
    
    try:
        # Method 1: Direct lookup
        chat = await bot.get_chat(f"@{username}")
        return chat.id
    except:
        pass
    
    try:
        # Method 2: Search
        chat = await bot.search_public_chat(username)
        return chat.id
    except:
        return None

def validate_token(token):
    """Check if admin bot token works"""
    resp = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
    return resp.get('ok', False)
