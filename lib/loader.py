# -*- coding: utf-8 -*-
import json
from os import path, getenv
from typing import Optional
from lib.common.services import log

BASE_PATH = path.dirname(path.abspath("{}/../".format(__file__)))
CONFIG_FILE_NAME = "config.json"
TEMPLATES_DIR = "lib/templates"


class Config:

    def __init__(self):
        self.configs = None
        try:
            # load configs from file
            with open(path.join(BASE_PATH, CONFIG_FILE_NAME), 'r') as conf:
                self.configs = json.load(conf)
        except Exception as e:
            log.warnings(__file__, Config.__name__, e)

    def get(self, key: str, default=None, json_format=False):
        # read from environment
        value = getenv(key)
        if value:
            # if key exist in environment
            # TODO: using of eval function , can be critical !
            return eval(value.title()) if value.lower() in ['false', 'true'] else value

        # read from file
        if self.configs:
            if not json_format:
                # split keys
                keys = key.strip().split(".")

                # we should have some keys
                if len(keys) == 0:
                    return default

                result = self.configs.get(keys[0])
                # follow keys to respond value
                for val in keys[1:]:
                    if type(result) is dict:
                        result = result.get(val)

                if result is None:
                    # we pass default value
                    return default
                else:
                    # pass result (we can obtain dictionary too)
                    return result
            else:
                # if key exist in file
                return self.configs.get(key, default)

        # return default
        return default


def template_loader(template: str) -> Optional[str]:
    try:
        # define template path
        templates_path = path.join(BASE_PATH, TEMPLATES_DIR)

        # add template name to template path
        t_path = path.join(templates_path, template)

        # load te from file
        with open(t_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        log.warnings(__file__, Config.__name__, e)
    return None
