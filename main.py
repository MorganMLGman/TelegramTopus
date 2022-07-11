import logging

from bot import TelegramBot

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("telegram_bot")
log_stream = logging.StreamHandler()
log_format = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
log_stream.setFormatter(log_format)
logger.handlers = []
logger.addHandler(log_stream)
logger.setLevel(logging.DEBUG)
#



def main(): 
    bot = TelegramBot()
    bot.start()

if __name__ == "__main__":
    main()