import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Your admin bot token
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))  # Your Telegram ID
TARGET_GROUP_ID = os.getenv('TARGET_GROUP_ID')  # -1001234567890
