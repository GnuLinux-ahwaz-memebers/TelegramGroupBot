class Command:
    def __init__(self, cmd: str, function):
        self.cmd = "!{}".format(cmd.lower())
        self.function = function

    def run(self, bot, update):
        self.function(bot, update)
