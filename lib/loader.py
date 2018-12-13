import json
from os import path,getenv


from lib.messages import log

BASE_PATH = path.dirname(path.abspath("{}/../".format(__file__)))
CONFIG_FILE_NAME = "config.json"

class config:

    def __init__(self):
        self.configs = None
        try:
            # load configs from file
            with open(path.join(BASE_PATH,CONFIG_FILE_NAME) , 'r') as conf:
                self.configs = json.load(conf)
        except Exception as e:
            log.warnings(__file__, config.__name__, e)

    def get(self,key,default = None):
        # read from environment
        value = getenv(key)
        if value :
            # if key exist in environment
            # TODO: using of eval function , can be critical !
            return eval(value.title()) if value.lower() in ['false','true'] else value

        # read from file
        if self.configs:
            # if key exist in file
            return self.configs.get(key,default)

        # return default
        return default
