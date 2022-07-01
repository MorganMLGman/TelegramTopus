from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm Telegram Bot to help you manage your self hosted server.")
    
async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Current server time: {datetime.now()}")