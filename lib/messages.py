import logging

logging.basicConfig(format='%(message)s', level=logging.ERROR)

class log:
    @staticmethod
    def error(file , function , msg):
        logging.error("EXCEPTION [{} - '{}' function] - {}".format(file , function , msg))
    @staticmethod
    def info(msg):
        result = "[*] {}".format(msg)
        print(result)
        logging.info(result)

class Messages:
    START_MESSAGE = 'HELP MESSAGE'