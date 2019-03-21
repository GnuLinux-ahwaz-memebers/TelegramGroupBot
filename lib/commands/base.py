import telegram
from lib.commands.helper import getGroupAdminsId, admin_required, messageRemover, group_command
from lib.common.services import log
from lib.common.template import GROUP_LINK, SMART_QUESTION_LINK, TOR_INSTALLATION_LINK, GROUP_LINK_DISABLED, FARSI, \
    GRUB_REPAIR, ASK_QUESTION, KALI, ABOUT, USAGE
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


@group_command
def __get_chat_id(bot, update):
    # print info in terminal
    log.info("Group.name: '{}' , Group.id: '{}'".format(
        update.message.chat.title,
        update.message.chat_id)
    )
    # delete command
    messageRemover(bot, update.message)


@group_command
def group_link(bot, update):
    # TODO: we can turn off/on it with dynamic methods like send a command to turn off it
    if Config().get('features.GROUP_LINK_ENABLE', False):

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


@group_command
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


@group_command
@admin_required
def spam(bot, update):
    # get tagged Message
    message = update.message.reply_to_message

    # delete tagged message
    messageRemover(bot, message)


@group_command
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


def smart_question(bot, update):
    # Get link from templates
    __passContent(bot, update, SMART_QUESTION_LINK.read())


def tor_installation(bot, update):
    # Get link from templates
    __passContent(bot, update, TOR_INSTALLATION_LINK.read())


def farsi(bot, update):
    # Get link from templates
    __passContent(bot, update, FARSI.read())


def grub_repair(bot, update):
    # Get link from templates
    __passContent(bot, update, GRUB_REPAIR.read())


def ask_question(bot, update):
    # Get link from templates
    __passContent(bot, update, ASK_QUESTION.read())


def kali(bot, update):
    # Get link from from templates
    __passContent(bot, update, KALI.read())


def about(bot, update):
    # Get link from from templates
    __passContent(bot, update, ABOUT.read())


def usage(bot, update):
    # Get link from from templates
    __passContent(bot, update, USAGE.read())
