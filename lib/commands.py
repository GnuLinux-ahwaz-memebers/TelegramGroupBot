from lib.messages import Messages


def help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=Messages.START_MESSAGE
    )