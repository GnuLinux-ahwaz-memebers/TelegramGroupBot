from lib.commands.helper import getGroupAdminsId, admin_required, messageRemover
from lib.loader import config

def group_link(bot,update):
    # Get Group link from config file
    GroupLink = config().get('GROUP_LINK', "No Link")
    # get tagged Message
    message = update.message if update.message else update.message.reply_to_message
    # Return Group Link
    bot.send_message(
        reply_to_message_id=message.message_id,
        chat_id=update.message.chat_id,
        text=GroupLink
    )

def report(bot,update):
    # get tagged Message
    message = update.message.reply_to_message
    # delete ![command] message
    messageRemover(bot, update.message)
    # get chat_id of admins group
    admins_group_chat_id = config().get('ADMINS_GROUP_CHAT_ID',None)
    if admins_group_chat_id:
        bot.forward_message(
            chat_id= admins_group_chat_id,
            from_chat_id= update.message.chat_id,
            message_id= message.message_id
        )


@admin_required
def spam(bot,update):
    # get tagged Message
    message = update.message.reply_to_message
    # delete tagged message
    messageRemover(bot, message)

@admin_required
def kick(bot,update):
    # get tagged Message
    message = update.message.reply_to_message
    # delete tagged message
    if messageRemover(bot,message):
        # Just others can removed (except admins) !
        if message.from_user.id not in getGroupAdminsId(bot, update):
            # Kick User of tagged Message
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=message.from_user.id
            )