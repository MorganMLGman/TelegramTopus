import logging

from bot import TelegramBot

# Logging
global logger 
logger = logging.getLogger("telegram_main")
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