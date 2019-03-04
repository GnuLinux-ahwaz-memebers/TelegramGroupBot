from lib.commands.base import group_link, report, kick, spam, smart_question, tor_installation
from lib.commands.helper import __get_chat_id
from lib.commands.model import Command
from lib.loader import Config
from lib.triggers.alwaysOn import link_remover

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
    Command("report", report)
]

if Config().get('ENABLE_GET_CHAT_ID', False):
    COMMANDS.append(Command("id", __get_chat_id))


# Listen on Messages
def dispatcher(bot, update):
    # Link Remover
    link_remover(bot, update)
    # Commands Handler
    for command in COMMANDS:
        if command.cmd == update.message.text:
            command.run(bot, update)
