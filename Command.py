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
        super().__init__()
        self.validArgs = ["-c", "-d"]
        self.passedArgs = []
        self.sys = sys
        self.path = ""

    def execute(self):
        print("CD command executed")
        if self.path == "":
            print("No path specified - staying in current directory")
        elif self.sys.is_path(self.path):
            print(f"Changing directory to: {self.path}")
        else:
            print(f"Invalid path: {self.path}")
        if self.passedArgs:
            print(f"Arguments: {self.passedArgs}")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.path = ""

        for arg in s:
            if arg[0] != "-":  # This is a path, not an option
                self.path = arg
            elif arg in self.validArgs:
                self.passedArgs.append(arg)
            else:
                print(f"Wrong argument: {arg}")
                return -1
        return 0


class LSCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-l", "-s"]
        self.passedArgs = []
        self.sys = sys
        self.path = ""

    def execute(self):
        print("LS command executed")
        if self.path == "":
            print("Listing current directory")
        elif self.sys.is_path(self.path):
            print(f"Listing directory: {self.path}")
        else:
            print(f"Invalid path: {self.path}")
        if self.passedArgs:
            print(f"Arguments: {self.passedArgs}")
        print("file1.txt  file2.txt  directory1/")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.path = ""

        for arg in s:
            if arg[0] != "-":
                self.path = arg
            elif arg in self.validArgs:
                self.passedArgs.append(arg)
            else:
                print(f"Wrong argument: {arg}")
                return -1
        return 0


class EXITCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys

    def execute(self):
        print("Exiting emulator...")
        self.sys.exit()

    def ParseArgs(self, s):
        self.passedArgs = []
        if len(s) != 0:
            print("Error: exit command takes no arguments")
            return -1
        return 0


class WRONGCommand(Command):
    def __init__(self):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []

    def execute(self):
        print("Error: Wrong command. Available commands: cd, ls, exit")

    def ParseArgs(self, s):
        return 0