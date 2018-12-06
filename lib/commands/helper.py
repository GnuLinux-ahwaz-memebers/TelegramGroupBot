from lib.messages import log

def getGroupAdminsId(bot,update):
    admins = bot.getChatAdministrators(
                chat_id=update.message.chat_id
            )
    return [admin.user.id for admin in admins]

def admin_required(func):
    def wrapper(*args, **kwargs):
        try:
            bot,update = args
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