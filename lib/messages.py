import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)


class log:
    @staticmethod
    def error(file, function, msg, EXIT=False):
        logging.error("Error: EXCEPTION [{} - '{}' function] - {}".format(file, function, msg))
        if EXIT:
            exit(code=10)

    @staticmethod
    def warnings(file, function, msg):
        logging.warning("Warning: [{} - '{}' function] - {}".format(file, function, msg))

    @staticmethod
    def info(msg):
        result = "[*] {}".format(msg)
        logging.info(result)


class Messages:
    START_MESSAGE = 'HELP MESSAGE'
    WELCOME = "کاربر {USER} لطفا ورود خود را تایید کنید در غیر اینصورت بعد از {TIME} دقیقه از گروه حذف خواهید شد."
    REGISTERATION_ACCEPTED = "عضویت شما تایید شد"
    ANSWER_DENY = "فقط کاربر تگ شده 🙂"
    REGISTERATION_VERIFY_BUTTON = 'تایید عضویت'