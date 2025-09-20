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
        self.factory_command["$"] = os.getenv
        self.commands = ["cd", "ls", "exit"]
    def execute(self):
        self.sys.is_running = True
        s = ""
        args = ""
        while self.sys.is_running:
            print(self.id, end="")
            s = input().split()
            args = ""
            if(len(s) != 1):
                args = s[1:]

            if self.factory_command[s[0]].ParseArgs(args) == -1:
                print("wrong arguments")
            else:
                self.factory_command[s[0]].execute()

