class Command:
    def __init__(self,cmd,function):
        self.cmd = "!{}".format(cmd)
        self.function = function

    def run(self,bot,update):
        self.function(bot,update)