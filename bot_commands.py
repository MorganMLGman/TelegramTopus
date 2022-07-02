from telegram import Update
from telegram.ext import ContextTypes
from commands import Commands


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_text =  \
"""Hello, I'm Telegram Bot to help you manage your self hosted server.

Available commands:
"""
    with open("command_list.txt", "r") as commands:
        lines = commands.readlines()
        for line in lines:
            msg_text += f"\t\t{line}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)
    
async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Current server time: {Commands.get_time()}")
    
async def get_uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bootTime, uptime = Commands.get_uptime()
        
    mm, ss = divmod(uptime, 60)
    hh, mm = divmod(mm, 60)
    dd, hh = divmod(hh, 24)
    ss = round(ss, 2)
    out = f"""
Boot time: {bootTime}
Days: {dd}
Hours: {hh}
Minutes: {mm}
Seconds: {ss}"""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=out)