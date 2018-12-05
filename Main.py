from lib import commands
from lib.base import Bot


# Init Bot
bot = Bot()

# add Handlers
bot.addHandler(commands.help,'help')


# start bot
bot.start(webhook=False)