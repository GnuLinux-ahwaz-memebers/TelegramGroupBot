from lib.commands.helper import getGroupAdminsId, admin_required, messageRemover
from lib.loader import Config


def __passLink(bot, update, link):
    # get tagged Message
    message = update.message.reply_to_message if update.message.reply_to_message else update.message
    # Return Link
    bot.send_message(
        reply_to_message_id=message.message_id,
        chat_id=update.message.chat_id,
        text=link
    )


def group_link(bot, update):
    # Get Group link from config file
    GroupLink = Config().get('GROUP_LINK', "No Link")
    __passLink(bot, update, GroupLink)


def smart_question(bot, update):
    # Get link from config file
    SmartQuestionLink = Config().get('SMART_QUESTION_LINK', "https://wiki.ubuntu.ir/wiki/Smart_Questions")
    __passLink(bot, update, SmartQuestionLink)


def tor_installation(bot, update):
    # Get link from config file
    TorLink = Config().get('TOR_INSTALLATION_LINK', "https://molaei.org/tor-ubuntu/")
    __passLink(bot, update, TorLink)


def report(bot, update):
    # get tagged Message
    message = update.message.reply_to_message
    # delete ![command] message
    messageRemover(bot, update.message)
    # get chat_id of admins group
    admins_group_chat_id = Config().get('ADMINS_GROUP_CHAT_ID', None)
    if admins_group_chat_id:
        bot.forward_message(
            chat_id=admins_group_chat_id,
            from_chat_id=update.message.chat_id,
            message_id=message.message_id
        )


@admin_required
def spam(bot, update):
    # get tagged Message
    message = update.message.reply_to_message
    # delete tagged message
    messageRemover(bot, message)


@admin_required
def kick(bot, update):
    # get tagged Message
    message = update.message.reply_to_message
    # delete tagged message
    if messageRemover(bot, message):
        # Just others can removed (except admins) !
        if message.from_user.id not in getGroupAdminsId(bot, update):
            # Kick User of tagged Message
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=message.from_user.id
            )