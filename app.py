from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, render_template, request
import asyncio
import sys
import os

# Fix import paths (files are in the same folder, not in utils/)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import BOT_TOKEN, ADMIN_USER_ID, TARGET_GROUP_ID
from User_hunter import get_user_id
from takeover import full_takeover

app = Flask(__name__)

# ====================== Telegram Bot Handlers ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Unauthorized")
        return
    
    await update.message.reply_text("""
🤖 Spector Telegram Bot Active!

Commands:
/hack @username - Full takeover
/id @username - Get user ID
/status - Bot status
    """)

async def hack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /hack @username")
        return
    
    username = context.args[0].replace('@', '')
    
    await update.message.reply_text(f"🔄 Starting takeover on @{username}...")
    
    try:
        result = await full_takeover(BOT_TOKEN, username, TARGET_GROUP_ID)
        status_emoji = "✅" if result.get('status') == 'success' else "❌"
        await update.message.reply_text(f"{status_emoji} {result.get('message', 'Done')}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ====================== Flask Web Dashboard ======================
@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/hack', methods=['POST'])
def web_hack():
    username = request.form.get('username', '').lstrip('@')
    if not username:
        return "<h1>Error: Username required</h1>"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(full_takeover(BOT_TOKEN, username, TARGET_GROUP_ID))
        return f"<h1>Result: {result}</h1>"
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

# ====================== Main ======================
def main():
    # Start Telegram Bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hack", hack_command))
    
    print("🤖 Bot is starting... Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    # Run both Flask and Telegram bot? 
    # For now, run only Telegram bot (Flask needs separate thread)
    main()
