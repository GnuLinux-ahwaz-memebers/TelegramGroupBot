from lib.commands.base import group_link, report, kick, spam
from lib.triggers.alwaysOn import link_remover


# Listen on Messages
def dispatcher(bot, update):
    # Link Remover
    link_remover(bot,update)

    # Commands Handler
    if update.message.text == "!link":
        # Send Group Link
        group_link(bot,update)
    if update.message.text == "!report":
        # Report Tagged Message
        report(bot,update)
    if update.message.text == "!kick":
        # Remove Tagged Message and Kick User of Tagged Message
        kick(bot,update)
    if update.message.text == "!spam":
        # Remove Tagged Message
        spam(bot,update)
