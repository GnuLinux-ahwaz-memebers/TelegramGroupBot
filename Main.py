from lib.bot import Bot
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
from lib import  handler
from lib.triggers import alwaysOn
from lib.triggers.alwaysOn import callback_handler


# Init Bot

bot = Bot()

# add Triggers
bot.addHandler(
    MessageHandler,
    alwaysOn.bots,
    Filters.status_update.new_chat_members,
    pass_job_queue=True
)

# add Handler
bot.addHandler(
    MessageHandler,
    handler.dispatcher,
    Filters.text,
)

# callback handler
bot.addHandler(
    CallbackQueryHandler,
    callback_handler
)

# start bot
bot.start()