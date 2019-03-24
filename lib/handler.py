from lib.commands.base import group_link, report, kick, spam, smart_question, tor_installation, farsi, ask_question, \
    kali, grub_repair, about, usage, __get_chat_id
from lib.commands.model import Command
from lib.loader import Config
from lib.triggers.listeners import telegram_link_remover

COMMANDS = [
    # Command("COMMAND_NAME",FUNCTION)
    # Command Usage : ![command]

    # Send Group Link (!link)
    Command("link", group_link),

    # Send Smart Question Link (!smart)
    Command("smart", smart_question),

    # Send Tor Installation Link (ubuntu) (!tor)
    Command("tor", tor_installation),

    # Remove Tagged Message and Kick User of Tagged Message (!kick)
    Command("kick", kick),

    # Remove Tagged Message (!spam)
    Command("spam", spam),

    # Report Tagged Message (!report)
    Command("report", report),

    # Type Farsi (!farsi)
    Command("farsi", farsi),

    # Ask Question in one Message Please (!ask)
    Command("ask", ask_question),

    # Don't Use Kali (!kali)
    Command("kali", kali),

    # Grub Repair (!grub)
    Command("grub", grub_repair),

    # About (!about)
    Command("about", about),

    # Bot Usage (!usage)
    Command("usage", usage),

]

if Config.get('GENERAL.ENABLE_GET_CHAT_ID', False):
    COMMANDS.append(Command("id", __get_chat_id))


# Listen on Messages
def dispatcher(bot, update):
    # Link Remover
    telegram_link_remover(bot, update)

    # Commands Handler
    if str(update.message.text).startswith("!"):
        for command in COMMANDS:
            if command.cmd == update.message.text:
                command.run(bot, update)
