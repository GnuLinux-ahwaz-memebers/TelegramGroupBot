import re
from lib.common.services import log


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
    if message is not None:
        # delete Message
        bot.delete_message(
            chat_id=message.chat_id,
            message_id=message.message_id
        )
        return True
    return False


def __get_chat_id(bot, update):
    # print info in terminal
    log.info("{} : {}".format(
        update.message.chat.title,
        update.message.chat_id)
    )
    # delete command
    messageRemover(bot, update.message)


def admin_required(func):
    def wrapper(*args, **kwargs):
        try:
            bot, update = args
            admins = getGroupAdminsId(*args)
            # delete ![command] message
            messageRemover(bot, update.message)
            # Check User is Admin or Not
            if update.message.from_user.id not in admins:
                return None
        except Exception as e:
            log.error(__file__, 'admin_required', e)

        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def remove_joined_leave_message(func):
    def wrapper(*args, **kwargs):
        try:
            # TODO: i think it's not safe
            bot, update = args[0:2]
            # Check User is Admin or Not
            if update.message.new_chat_members or update.message.left_chat_member:
                messageRemover(bot, update.message)
        except Exception as e:
            log.error(__file__, 'remove_joined_leave_message', e)

        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def link_finder(text):
    telegram_links_regex = r"http(s?)\:\/\/t\.me/[\w\/]+"
    return re.search(telegram_links_regex, text)
