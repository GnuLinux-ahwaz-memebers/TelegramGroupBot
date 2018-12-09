from lib.messages import log
import re

def getGroupAdminsId(bot,update):
    admins = bot.getChatAdministrators(
                chat_id=update.message.chat_id
            )
    return [admin.user.id for admin in admins]

def restrictUser(bot,update,user,restrict = True):
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

def messageRemover(bot,message):
    if message is not None:
        # delete Message
        bot.delete_message(
            chat_id=message.chat_id,
            message_id=message.message_id
        )
        return True
    return False

def __get_chat_id(update):
    print(update.message.chat_id)

def admin_required(func):
    def wrapper(*args, **kwargs):
        try:
            bot,update = args
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

def link_finder(text):
    TELEGRAM_LINKS_REGEX = r"http(s?)\:\/\/t\.me/[\w\/]+"
    return re.search(TELEGRAM_LINKS_REGEX,text)