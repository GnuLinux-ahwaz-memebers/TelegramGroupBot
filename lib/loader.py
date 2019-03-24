# -*- coding: utf-8 -*-
import json
from os import path, getenv, pardir
from pathlib import Path
from typing import Optional
from lib.common.services import log
from configparser import ConfigParser

BASE_PATH = path.join(path.abspath(path.dirname(__file__)), pardir)
CONFIG_FILE_NAME = "config.ini"
TEMPLATES_DIR = "lib/templates"


class Config:
    _instance = None

    def __init__(self):
        if Config._instance:
            return
        log.info("Reading config file")
        self.configs = None
        try:
            # load configs from file
            config_path = path.join(BASE_PATH, CONFIG_FILE_NAME)
            self.configs = ConfigParser()
            self.configs.read(config_path)
        except Exception as e:
            log.warnings(__file__, Config.__name__, e)

    @staticmethod
    def getInt(key: str, default=None):
        return int(Config.get(key,default))

    @staticmethod
    def getFloat(key: str, default=None):
        return float(Config.get(key,default))

    @staticmethod
    def getString(key: str, default=None):
        return str(Config.get(key, default))

    @staticmethod
    def get(key: str, default=None):

        if len(key) == 0 or '.' not in key == 0:
            return default

        if not Config._instance:
            Config._instance = Config()

        # read from environment
        value = getenv(key)
        if value:
            # ignore config if key exists in environment, convert too bool type if possible
            return value.lower() == 'true' if value.lower() in ['false', 'true'] else value

        keys = key.strip().split(".")
        value = default
        try:
            value = Config._instance.configs[keys[0]]
            for k in keys[1:]:
                value = value[k]
            if value.lower() in ['false', 'True']:
                return value.lower() == 'true'
            return value
        except:
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
