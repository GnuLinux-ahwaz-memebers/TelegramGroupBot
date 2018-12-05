import json
import os

from lib.messages import log

BASE_PATH = os.path.dirname(os.path.abspath("{}/../".format(__file__)))
CONFIG_FILE_NAME = "config.json"

def config():
    try:
        with open(os.path.join(BASE_PATH,CONFIG_FILE_NAME) , 'r') as conf:
            return json.load(conf)
    except Exception as e:
        log.error(__file__,config.__name__,e)