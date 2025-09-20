import abc

import My_System


class Command(abc.ABC):


    def __init__(self):
        self.validArgs = []
        self.passedArgs = []

    def execute(self):
        pass

    def ParseArgs(self, s):
        if s not in self.validArgs:
            return -1
        self.passedArgs = s
        return 0


class CDCommand(Command):

    def __init__(self, sys: My_System):
        self.validArgs = ["-c", "-d"] # пока примерные аргументы. При реализации команд список изменится
        self.passedArgs = []
        self.sys = sys
        self.path = ""


    def execute(self):
        print("i am ls\n")
        if self.path == "":
            print("")
        elif self.sys.is_path(self.path):
            print("path is Correct")
        else:
            print("path is Uncorrect")
        print("Arguments", self.passedArgs)

    def ParseArgs(self, s):
        self.passedArgs = []
        if len(s) != 0 and s[0][0] == "/":
            self.path = s[0]
            s = s[1:]
        if len(s) != 0:
            if(len(s) > 1):
                if s not in self.validArgs:
                    return -1
                else:
                    self.passedArgs = s
        return 0

class LSCommand(Command):

    def __init__(self, sys: My_System):
        self.validArgs = ["-l", "-s"]  # пока примерные аргументы. При реализации команд список изменится
        self.passedArgs = []
        self.sys = sys
        self.path = ""


    def execute(self):
        print("i am ls\n")
        if self.path == "":
            print("")
        elif self.sys.is_path(self.path):
            print("path is Correct")
        else:
            print("path is Uncorrect")
        print("Arguments", self.passedArgs)

    def ParseArgs(self, s):
        self.passedArgs = []
        if len(s) != 0 and s[0][0] == "/":
            self.path = s[0]
            s = s[1:]
        if len(s) != 0:
            if (len(s) > 1):
                if s not in self.validArgs:
                    return -1
                else:
                    self.passedArgs = s
        return 0

class EXITCommand(Command):

    def __init__(self, sys: My_System):
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys

    def execute(self):
        self.sys.exit()

    def ParseArgs(self, s):
        self.passedArgs = []
        if len(s) != 0:
            return -1
        return 0

class WRONGCommand(Command):

    def __init__(self):
        self.validArgs = []
        self.passedArgs = []

    def execute(self):
        print("Wrong command")

    def ParseArgs(self, s):
        return 0