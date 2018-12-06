from lib.commands.base import group_link, report


def commands_dispatcher(bot,update):
    # Commands Handler
    if update.message.text == "!link":
        # Send Group Link
        group_link(bot,update)
    if update.message.text == "!report":
        # Report Tagged Message
        report(bot,update)
