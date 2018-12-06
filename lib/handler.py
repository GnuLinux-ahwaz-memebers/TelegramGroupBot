from lib.commands.base import group_link, report
from lib.triggers.alwaysOn import link_remover


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
