import telegram
from lib.commands.helper import getGroupAdminsId, admin_required, messageRemover
from lib.common.services import log
from lib.common.template import GROUP_LINK, SMART_QUESTION_LINK, TOR_INSTALLATION_LINK, GROUP_LINK_DISABLED
from lib.loader import Config


def __passContent(bot, update, content, **kwargs):
    # get mentioned Message if exists
    message = update.message.reply_to_message \
        if update.message.reply_to_message \
        else update.message

    # Return Link
    bot.send_message(
        reply_to_message_id=message.message_id,
        chat_id=update.message.chat_id,
        text=content,
        parse_mode=telegram.ParseMode.MARKDOWN,
        **kwargs
    )


def group_link(bot, update):
    # TODO: we can turn off/on it with dynamic methods like send a command to turn off it
    if Config().get('features', {}).get('GROUP_LINK_ENABLE', False):

        # Get Group link from templates
        invite_link = bot.getChat(
            chat_id=update.message.chat_id
        ).invite_link

        # if link doesn't exist for this bot so we create it
        if invite_link is None:
            invite_link = bot.export_chat_invite_link(
                chat_id=update.message.chat_id
            )

        # pass invite link to template
        content = GROUP_LINK.read().format(INVITE_LINK=invite_link)
    else:
        # TODO: revoke the previous invite link
        # bot.export_chat_invite_link(
        #        chat_id=update.message.chat_id
        #    )
        content = GROUP_LINK_DISABLED.read()

    __passContent(bot, update, content)


def smart_question(bot, update):
    # Get link from from templates
    SmartQuestionLink = SMART_QUESTION_LINK.read()
    __passContent(bot, update, SmartQuestionLink)


def tor_installation(bot, update):
    # Get link from from templates
    TorLink = TOR_INSTALLATION_LINK.read()
    __passContent(bot, update, TorLink)


def report(bot, update):
    # get tagged Message
    message = update.message.reply_to_message

    # delete ![command] message
    messageRemover(bot, update.message)
    try:
        # get chat_id of admins group
        admins_group_chat_id = Config().get('ADMINS_GROUP_CHAT_ID', 0)
        if admins_group_chat_id != 0:
            bot.forward_message(
                chat_id=admins_group_chat_id,
                from_chat_id=update.message.chat_id,
                message_id=message.message_id
            )
        else:
            log.error(__file__, 'report', "you don't set ADMINS_GROUP_CHAT_ID in configuration yet")
    except Exception as e:
        log.error(__file__, 'report', e)


@admin_required
def spam(bot, update):
    # get tagged Message
    message = update.message.reply_to_message

    # delete tagged message
    messageRemover(bot, message)

    # delete ![command] message
    messageRemover(bot, update.message)


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
