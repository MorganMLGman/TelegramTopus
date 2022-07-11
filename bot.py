from decouple import config
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

import bot_commands as bot_cmd


class TelegramBot:
    __TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
    
    def __init__(self) -> None:
        self.application = ApplicationBuilder().token(self.__TELEGRAM_TOKEN).build()
    
        self.application.add_handlers([
            CommandHandler('start', bot_cmd.start),
            CommandHandler('time', bot_cmd.get_time),
            CommandHandler('uptime', bot_cmd.get_uptime),
            CommandHandler('load', bot_cmd.get_load),
            CommandHandler('cpu_temp', bot_cmd.get_temps),
            CommandHandler('set_host', bot_cmd.set_host),
            CallbackQueryHandler(bot_cmd.keyboard_handler)
        ])
        
    def start(self):
        self.application.run_polling()