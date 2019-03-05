import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lib.commands.base import messageRemover
from lib.commands.helper import link_finder, restrictUser, remove_joined_leave_message
from lib.common.messaging import Messages, Templates
from lib.common.services import log
from lib.loader import Config


def register_timer(bot, job):
    try:
        # get information
        chat_id = job.context.get('chat_id')

        # possible message delete
        message = job.context.get('message')

        # possible user leave the group
        user_id = job.context.get('user_id')

        # remove message
        if message:
            # possible message delete
            messageRemover(bot, message)

        # remove user
        if user_id:
            # possible user leave the group
            bot.kick_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
    except Exception as e:
        log.error(__file__, 'register_timer', e)


def callback_handler(bot, update):
    if update.callback_query.data == str(update.callback_query.from_user.id):
        # get welcome message
        message = update.callback_query.message

        # remove welcome message
        messageRemover(bot, message)

        # registration accepted nag
        out_message = Messages.load(Templates.REGISTRATION_ACCEPTED)

        # unrestricted user
        restrictUser(bot, update.callback_query, update.callback_query.from_user, False)
    else:
        # don't touch =)
        out_message = Messages.load(Templates.JUST_TAGGED_USER)

    bot.answerCallbackQuery(
        callback_query_id=update.callback_query.id,
        text=out_message
    )


def registration_verification(bot, update, job_queue, user):
    commands = [
        [InlineKeyboardButton(
            Messages.load(Templates.REGISTRATION_VERIFY_BUTTON),
            callback_data=str(user.id)
        )],
    ]
    reply_markup = InlineKeyboardMarkup(commands)

    user_info = "[{}](tg://user?id={})".format(
        user.username if user.username else user.first_name,
        user.id
    )

    # timer should be a number (we wanna use integer)
    timer = Config().get('REGISTER_TIMER_MINUTES', 1)
    timer = int(timer) if not timer.isdecimal() else 1

    message = bot.send_message(
        chat_id=update.message.chat_id,
        text=Messages.load(Templates.WELCOME).format(
            USER=user_info,
            TIME=timer
        ),
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

    # add to job queue
    job_queue.run_once(
        register_timer,
        timer * 60,
        context={
            "chat_id": update.message.chat_id,
            "message": message,
            "user_id": user.id
        }
    )


@remove_joined_leave_message
def bots(bot, update, job_queue):
    for user in update.message.new_chat_members:
        # Remove Bot
        if user.is_bot:
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=user.id
            )
            # Kick User who add bot !
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=update.message.from_user.id
            )
        # restrict user
        restrictUser(bot, update, user)
        # check user is bot or not (verify a question)
        registration_verification(bot, update, job_queue, user)


def link_remover(bot, update):
    # TODO: We should be handle url shorter later!
    # find Telegram Links
    if link_finder(update.message.text):
        # Remove Message
        if Config().get('GROUP_LINK', 'No link').strip() != update.message.text.strip():
            messageRemover(bot, update.message)
