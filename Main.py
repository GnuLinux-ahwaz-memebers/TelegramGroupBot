from lib.bot import Bot
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
from lib import handler
from lib.triggers import listeners
from lib.triggers.features.controller import features_handler
from lib.triggers.listeners import callback_handler

# Init Bot
bot = Bot()

# add Triggers
bot.addHandler(
    MessageHandler,
    listeners.bots,
    Filters.status_update,
    pass_job_queue=True
)
# features_handler
bot.addHandler(
    MessageHandler,
    features_handler,
    Filters.photo
)


# add Handler
bot.addHandler(
    MessageHandler,
    handler.dispatcher,
    Filters.all,
)

# callback handler
bot.addHandler(
    CallbackQueryHandler,
    callback_handler
)

# start bot
bot.start()
