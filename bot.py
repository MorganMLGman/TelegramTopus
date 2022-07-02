from decouple import config
from telegram.ext import ApplicationBuilder, CommandHandler

import bot_commands as bot_cmd


class TelegramBot:
    __TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
    
    def __init__(self) -> None:
        self.application = ApplicationBuilder().token(self.__TELEGRAM_TOKEN).build()
    
        start_handler = CommandHandler('start', bot_cmd.start)
        time_handler = CommandHandler('time', bot_cmd.get_time)
        uptime_handler = CommandHandler('uptime', bot_cmd.get_uptime)
        self.application.add_handler(start_handler)
        self.application.add_handler(time_handler)
        self.application.add_handler(uptime_handler)
        
    def start(self):
        self.application.run_polling()