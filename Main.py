from telegram.ext import MessageHandler, Filters

from lib.commands import  handler
from lib.bot import Bot


# Init Bot
bot = Bot()

# add Commands Handler
bot.addHandler(
    MessageHandler,
    Filters.text,
    handler.commands_dispatcher
)


# start bot
bot.start(webhook=False)