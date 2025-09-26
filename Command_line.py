import My_System
from Command import CDCommand, LSCommand, EXITCommand, WRONGCommand
import os

class CommandLine:
    def __init__(self, sys: My_System):
        self.sys = sys
        self.id = sys.User + "@" + sys.Comp + ":"
        self.command = ""
        self.factory_command = dict()
        self.factory_command['cd'] = CDCommand(sys)
        self.factory_command['ls'] = LSCommand(sys)
        self.factory_command["exit"] = EXITCommand(sys)
        self.factory_command["wrong"] = WRONGCommand()
        self.commands = ["cd", "ls", "exit"]
    def execute(self):
        self.sys.is_running = True
        s = ""
        args = ""
        while self.sys.is_running:
            print(self.id, end="")
            s = input().split()
            self.command = s[0]
            args = ""
            if self.command[0] == "$":
                value = os.getenv(self.command[0:])
                print("Value of 'HOME' environment variable :", value)
                continue
            if(len(s) != 1):
                args = s[1:]


            if s[0] not in self.commands:
                self.command = "wrong"

            if self.factory_command[self.command].ParseArgs(args) == -1:
                pass
            else:
                self.factory_command[self.command].execute()

