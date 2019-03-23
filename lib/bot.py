from telegram.ext import Updater
from lib import loader
from lib.common.services import log


class Bot:
    def __init__(self):
        # Define Base Variables
        self.CONFIG = loader.Config()
        try:
            if self.CONFIG.get('PROXY_ON', False):
                self.updater = Updater(
                    token=self.CONFIG.get('TOKEN'),
                    request_kwargs={
                        'proxy_url': self.CONFIG.get('PROXY_URL', 'http://localhost:8123')
                    }
                )
            else:
                self.updater = Updater(token=self.CONFIG.get('TOKEN'))

            self.dispatcher = self.updater.dispatcher
        except Exception as e:
            log.error(__file__, '__init__', e, True)

    def start(self, webhook=loader.Config().get('WEB_HOOK_ON', False)):
        try:
            if webhook:
                # Run Bot as webhook
                self.updater.start_webhook(
                    listen=self.CONFIG.get('WEB_HOOK_LISTEN', '0.0.0.0'),
                    port=self.CONFIG.get('WEB_HOOK_PORT', '8443'),
                    url_path=self.CONFIG.get('TOKEN')
                )
                self.updater.bot.set_webhook('{}{}'.format(
                    self.CONFIG.get('WEB_HOOK_ADDRESS', 'localhost'),
                    self.CONFIG.get('TOKEN'))
                )
                self.updater.idle()
            else:
                self.updater.start_polling()
            log.info("Bot Started...")
            if self.CONFIG.get('ENABLE_GET_CHAT_ID', False):
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
