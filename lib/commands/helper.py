import re
import telegram
from lib.common.services import log
from lib.common.template import IT_IS_SUPERGROUP_COMMAND
from lib.loader import Config


def getGroupAdminsId(bot, update):
    admins = bot.getChatAdministrators(
        chat_id=update.message.chat_id
    )
    return [admin.user.id for admin in admins]


def restrictUser(bot, update, user, restrict=True):
    # restrict User
    restrict = (not restrict)
    bot.restrict_chat_member(
        chat_id=update.message.chat_id,
        user_id=user.id,
        can_send_messages=restrict,
        can_send_media_messages=restrict,
        can_send_other_messages=restrict,
        can_add_web_page_previews=restrict,
    )


def messageRemover(bot, message):
    # safe remove (message should be exist)
    if type(message) is dict:
        bot.delete_message(
            chat_id=message.get('chat_id', 0),
            message_id=message.get('message_id', 0)
        )
        return True
    if message is not None:
        # delete Message
        bot.delete_message(
            chat_id=message.chat_id,
            message_id=message.message_id
        )
        return True
    return False


def admin_required(func):
    def wrapper(*args, **kwargs):
        try:
            bot, update = args
            admins = getGroupAdminsId(*args)
            # Check User is Admin or Not
            if update.message.from_user.id not in admins:
                return None
        except Exception as e:
            log.error(__file__, 'admin_required', e)

        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def group_command(func):
    def wrapper(*args, **kwargs):
        try:
            bot, update = args
            if update.message.chat.type.strip() != "supergroup":
                bot.send_message(
                    reply_to_message_id=update.message.message_id,
                    chat_id=update.message.chat_id,
                    text=IT_IS_SUPERGROUP_COMMAND.read(),
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    **kwargs
                )
                return None
        except Exception as e:
            log.error(__file__, 'group_command', e)

        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def remove_joined_leave_message(func):
    def wrapper(*args, **kwargs):
        try:
            # TODO: i think it's not safe
            bot, update = args[0:2]

            # don't effect self
            if update.message.left_chat_member:
                if bot.id == update.message.left_chat_member.id:
                    return None
            for user in update.message.new_chat_members:
                if bot.id == user.id:
                    return None

            if Config().get('features.REMOVE_STATUS_MESSAGES', False):
                # TODO: this has overlap with other usage of new_chat_members in functions that using this decorator
                # joined/leave/remove members messages
                if len(update.message.new_chat_members) > 0 or update.message.left_chat_member:
                    messageRemover(bot, update.message)
        except Exception as e:
            log.error(__file__, 'remove_joined_leave_message', e)

        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def link_finder(text):
    # TODO: improve it for other links
    telegram_links_regex = r"http(s?)\:\/\/t\.me/[\w\/]+"
    return re.search(telegram_links_regex, text)
