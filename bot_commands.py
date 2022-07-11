from turtle import home
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from commands import Commands, HostSystem


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
    
async def get_load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function reads system load using differents methods for different host systems,
    and sends it in a message.
    """
    if Commands.host_system == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="Unfortunately you need to set host system first, \
                                           before using this command. You can do this with /set_host")

    elif (HostSystem.FEDORA == Commands.host_system or
          HostSystem.UBUNTU == Commands.host_system or
          HostSystem.RASPBIAN == Commands.host_system):
          
            load1m, load5m, load15m = Commands.get_load()    
            out = f"""
Average load:
1 minute: {round(load1m, 2)}%
5 minutes: {round(load5m, 2)}%
15 minutes: {round(load15m, 2)}%"""

            await context.bot.send_message(chat_id=update.effective_chat.id, text=out)
            
    elif HostSystem.WINDOWS == Commands.host_system:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please wait 10 seconds, measurement started")
        load, _, _ = Commands.get_load()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Average CPU usage: {round(load, 2)}%")
        
    
async def get_temps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temps = Commands.get_temp()
    if temps:
        out = "Temperature:\n"
        for key, val in temps.items():
            match(key.lower()):
                case "wifi_card":
                    out += f"WiFi card: {val}\n"
                
                case "cpu":
                    out += "CPU:\n"
                    if isinstance(val, dict):
                        for key2, val2 in val.items():
                            out += f"\t\t{key2}: {val2}\n"
                    else: 
                        out += f"\t\tNo data available.\n"
                
                case "nvme_disk":
                    out += f"NVMe Disk: {val}\n"
            
        await context.bot.send_message(chat_id=update.effective_chat.id, text = out)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Unfortunately, the sensor data could not be read or your operating system is not supported.")
        
async def set_host(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """set_host Replies with inline keyboard"""
    keyboard = []
    
    for i in HostSystem:
        keyboard.append([InlineKeyboardButton(i.name, callback_data=i.name)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Please choose running OS:", reply_markup=reply_markup)
    
async def keyboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    
    await query.answer()
    
    match(query.data):
        case "FEDORA":
            Commands.host_system = HostSystem.FEDORA
        case "UBUNTU":
            Commands.host_system = HostSystem.UBUNTU
        case "RASPBIAN":
            Commands.host_system = HostSystem.RASPBIAN
        case "WINDOWS":
            Commands.host_system = HostSystem.WINDOWS           
    
    await query.edit_message_text(text=f"Selected OS: {query.data}")