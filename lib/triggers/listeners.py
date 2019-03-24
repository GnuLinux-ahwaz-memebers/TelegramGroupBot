import json
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lib.commands.base import messageRemover
from lib.commands.helper import link_finder, restrictUser, remove_joined_leave_message, getGroupAdminsId
from lib.common.template import REGISTRATION_ACCEPTED, JUST_TAGGED_USER, REGISTRATION_VERIFY_BUTTON, WELCOME, \
    GROUP_LINK, DELETE_REPORTED_MESSAGE_BUTTON, REPORT_MESSAGE, DELETE_REPORTED_MESSAGE
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

    data = json.loads(update.callback_query.data)
    reply_message = update.callback_query.message.reply_to_message

    # TODO: i change the data serialization but didn't test it work or not =)
    if update.callback_query.data == str(update.callback_query.from_user.id):
        # get welcome message
        message = update.callback_query.message

        # remove welcome message
        messageRemover(bot, message)

        # registration accepted nag
        out_message = REGISTRATION_ACCEPTED.read()

        # unrestricted user
        restrictUser(bot, update.callback_query, update.callback_query.from_user, False)

    elif reply_message and (data.get('fmsg_id', 0) == reply_message.message_id):
        # here messages (2 messages , forwarded and question)
        messageRemover(bot, {
            'chat_id': update.callback_query.message.chat_id,
            'message_id': data.get('fmsg_id')
        })
        messageRemover(bot, {
            'chat_id': update.callback_query.message.chat_id,
            'message_id': update.callback_query.message.message_id
        })
        # delete main forwarded messages from other chat_id
        messageRemover(bot, {
            'chat_id': data.get('chat_id', 0),
            'message_id': data.get('msg_id', 0)
        })

        out_message = DELETE_REPORTED_MESSAGE.read()
    else:
        # TODO: we should pass a suitable message
        out_message = "Delete self"
        messageRemover(bot, {
            'chat_id': update.callback_query.message.chat_id,
            'message_id': update.callback_query.message.message_id
        })

    # else:
    #     # don't touch =)
    #     out_message = JUST_TAGGED_USER.read()

    bot.answerCallbackQuery(
        callback_query_id=update.callback_query.id,
        text=out_message
    )


def registration_verification(bot, update, job_queue, user):
    # define button
    commands = [
        [InlineKeyboardButton(
            REGISTRATION_VERIFY_BUTTON.read(),
            callback_data=str(user.id)
        )],
    ]
    # create a markup
    reply_markup = InlineKeyboardMarkup(commands)

    # TODO: is it safe ? others can get information about logged in user
    #   Mitigation: it's better that show first name of joined user
    user_info = "[{}](tg://user?id={})".format(
        user.username if user.username else user.first_name,
        user.id
    )

    # timer should be a number (we wanna use integer)
    timer = Config.getInt('OPTIONS.REGISTER_TIMER_MINUTES', 1)

    # send verification message
    message = bot.send_message(
        chat_id=update.message.chat_id,
        text=WELCOME.read().format(
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
    # Multi User Invited Support
    for user in update.message.new_chat_members:
        # Remove Bot
        if user.is_bot:
            # Kick the bot
            bot.kick_chat_member(
                chat_id=update.message.chat_id,
                user_id=user.id
            )

            # if user not admin
            if update.message.from_user.id not in getGroupAdminsId(bot, update):
                # Kick User who add bot !
                bot.kick_chat_member(
                    chat_id=update.message.chat_id,
                    user_id=update.message.from_user.id
                )
        else:
            if Config.get('OPTIONS.LOGIN_RESTRICTION', False):
                # restrict user
                restrictUser(bot, update, user)

                # check user is bot or not (verify a question)
                registration_verification(bot, update, job_queue, user)


def telegram_link_remover(bot, update):
    # TODO: We should be handle url shorter later!
    if not Config.get('OPTIONS.TELEGRAM_LINK_REMOVER', False):
        return None

    # if message has a text type
    if bool(update.message.text):
        text = update.message.text

    # if message has a forward type
    elif bool(update.message.forward_date):
        text = update.message.caption

    else:
        return

    # find Telegram Links
    if link_finder(text):
        # Remove Message
        if GROUP_LINK.read() != text.strip():
            messageRemover(bot, update.message)


def reported_message_delete(bot, update, admins_group_chat_id, forwarded_message, message):
    # define button
    commands = [
        [InlineKeyboardButton(
            DELETE_REPORTED_MESSAGE_BUTTON.read(),
            # we can't use long keys (restricted by telegram: 1-64 bytes)
            callback_data=json.dumps({
                'chat_id': message.chat_id,
                'msg_id': message.message_id,
                'fmsg_id': forwarded_message.message_id
            })
        )],
    ]

    # create a markup
    reply_markup = InlineKeyboardMarkup(commands)

    bot.send_message(
        chat_id=admins_group_chat_id,
        text=REPORT_MESSAGE.read(),
        reply_to_message_id=forwarded_message.message_id,
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
