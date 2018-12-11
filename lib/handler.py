from lib.commands.base import group_link, report, kick, spam, smart_question, tor_installation
from lib.commands.model import Command
from lib.triggers.alwaysOn import link_remover



COMMANDS = {
    # Command("COMMAND_NAME",FUNCTION)
    # Send Group Link
    Command("link",group_link),
    # Send Smart Question Link
    Command("smart",smart_question),
    # Send Tor Installation Link (ubuntu)
    Command("tor",tor_installation),
    # Remove Tagged Message and Kick User of Tagged Message
    Command("kick",kick),
    # Remove Tagged Message
    Command("spam",spam),
    # Report Tagged Message
    Command("report",report)
}

# Listen on Messages
def dispatcher(bot, update):
    # Link Remover
    link_remover(bot,update)

    # Commands Handler
    for command in COMMANDS:
        if command.cmd == update.message.text:
            command.run(bot,update)
