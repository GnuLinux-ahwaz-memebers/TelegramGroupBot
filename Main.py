from lib.bot import Bot
from telegram.ext import MessageHandler, Filters
from lib import  handler
from lib.triggers import alwaysOn


# Init Bot
bot = Bot()

# add Triggers
bot.addHandler(
    MessageHandler,
    Filters.status_update.new_chat_members,
    alwaysOn.ban_bots
)

# add Handler
bot.addHandler(
    MessageHandler,
    Filters.text,
    handler.dispatcher
)

# start bot
bot.start(webhook=False)