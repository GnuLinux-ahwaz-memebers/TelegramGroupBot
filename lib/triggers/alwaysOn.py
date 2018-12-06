from lib.commands.base import messageRemover
from lib.commands.helper import link_finder
from lib.loader import config


def ban_bots(bot,update):
    for user in update.message.new_chat_members:
        # Remove Bot
        if user.is_bot:
            bot.kick_chat_member(
                chat_id = update.message.chat_id,
                user_id = user.id
            )
            # Kick User who add bot !
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=update.message.from_user.id
            )

def link_remover(bot,update):
    # TODO: We should handle url shorters !
    # find Telegram Links
    if link_finder(update.message.text):
        # Remove Message
        if config().get('GROUP_LINK','No link').strip() != update.message.text.strip():
            messageRemover(bot,update,update.message)
