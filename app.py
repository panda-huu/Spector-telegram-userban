from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, render_template, request
import asyncio
from config import BOT_TOKEN, ADMIN_USER_ID, TARGET_GROUP_ID
from utils.user_hunter import get_user_id
from utils.takeover import full_takeover

app = Flask(name)

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Unauthorized")
        return
    await update.message.reply_text("""
🤖 Telegram ID Hacker Bot Active!

Commands:
/hack @username - Full takeover
/id @username - Get user ID
/flood @username - Spam attack
/ban @username - Permanent ban
/status - Bot status
    """)

async def hack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /hack @username")
        return
    
    username = context.args[0].replace('@', '')
    result = await full_takeover(BOT_TOKEN, username, TARGET_GROUP_ID)
    
    status_emoji = "✅" if result['status'] == 'success' else "❌"
    await update.message.reply_text(f"{status_emoji} {result['message']}")

# Flask Web Dashboard
@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/hack', methods=['POST'])
def web_hack():
    username = request.form['username']
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(full_takeover(BOT_TOKEN, username.lstrip('@'), TARGET_GROUP_ID))
    return f"<h1>{result}</h1>"

def main():
    # Telegram Bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hack", hack_command))
    
    # Start bot
    print("🤖 Bot starting...")
    application.run_polling()

if"__name__" == 'main':
    main()
