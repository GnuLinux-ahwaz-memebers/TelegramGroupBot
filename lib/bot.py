from telegram.ext import Updater
from lib import loader
from lib.loader import Config
from lib.common.services import log

class Bot:
    def __init__(self):
        try:
            if Config.get('PROXY.ENABLED', False):
                self.updater = Updater(
                    token=Config.get('PROXY.ENABLED'),
                    request_kwargs={
                        'proxy_url': Config.get('PROXY.URL', 'http://localhost:8123')
                    }
                )
            else:
                self.updater = Updater(token=Config.get('GENERAL.TOKEN'))

            self.dispatcher = self.updater.dispatcher
        except Exception as e:
            log.error(__file__, '__init__', e, True)

    def start(self, webhook=Config.get('WEB_HOOK.ENABLED', False)):
        try:
            if webhook:
                # Run Bot as webhook
                self.updater.start_webhook(
                    listen=Config.get('WEB_HOOK.LISTEN', '0.0.0.0'),
                    port=Config.get('WEB_HOOK.PORT', '8443'),
                    url_path=Config.get('GENERAL.TOKEN')
                )
                self.updater.bot.set_webhook('{}{}'.format(
                    Config.get('WEB_HOOK.ADDRESS', 'localhost'),
                    Config.get('GENERAL.TOKEN'))
                )
                self.updater.idle()
            else:
                self.updater.start_polling()
            log.info("Bot Started...")
            if Config.get('GENERAL.ENABLE_GET_CHAT_ID', False):
                log.info("pass command `!id` in the admins group to get group_id here (not in the telegram) "
                         "and set it in ADMINS_GROUP_CHAT_ID variable "
                         "in the config.json file.")
        except Exception as e:
            log.error(__file__, 'start', e, True)

    def addHandler(self, handler, function, filter_=None, **args):
        try:
            if filter_:
                self.dispatcher.add_handler(handler(filter_, function, **args))
            else:
                self.dispatcher.add_handler(handler(function))
        except Exception as e:
            log.error(__file__, 'addHandler', e)
