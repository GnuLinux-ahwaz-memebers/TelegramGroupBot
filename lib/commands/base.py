from lib.commands.helper import getGroupAdminsId
from lib.loader import config

def group_link(bot,update):
    # Get Group link from config file
    bot.send_message(
        reply_to_message_id=update.message.chat_id,
        chat_id=update.message.chat_id,
        text=config().get('GROUP_LINK', "No Link")
    )

def messageRemover(bot,update,message):
    if message is not None:
        # delete Message
        bot.delete_message(
            chat_id=update.message.chat_id,
            message_id=message.message_id
        )
        return True
    return False

def report(bot,update):
    # get tagged Message
    message = update.message.reply_to_message

    # delete tagged message
    if messageRemover(bot,update,message):
        # delete ![command] message
        messageRemover(bot,update,update.message)
        # Just others can removed (except admins) !
        if message.from_user.id not in getGroupAdminsId(bot, update):
            # Kick User of tagged Message
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=message.from_user.id
            )