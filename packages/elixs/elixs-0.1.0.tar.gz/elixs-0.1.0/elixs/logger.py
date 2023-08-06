#Copyright (C)2022  Elias Kremer, full license (GNU AGPLv3) in LICENSE.txt
from .errorhandlers import *
from time import ctime as ct

class Logger:
    def __init__(self, config_obj, path, name, short = "LOGG"):
        self.short = short

        runmode = config_obj.getconfig("logmode")
        if runmode == "console":
            from sys import stderr
            self.out = stderr
        elif runmode == "logfile":
            from os.path import exists
            path += "/logs/"
            if not exists(path):
                from os import mkdir
                mkdir(path)
            self.out = open(path + name, "a")
        else:
            self.out = open("/dev/null", "a")

    def append(self, message):
        self.out.write(ct()[4:-5] + ": " + self.short + ": " + str(message) + "\n")
        self.out.flush()
        return True

    def close(self):
        self.out.flush()
        self.out.close()
        return True

def version():
    return 1.2 #Slightly modified version of 1.2
