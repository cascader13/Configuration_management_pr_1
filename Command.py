import abc
import My_System


class Command(abc.ABC): # абстрактный класс команды
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
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys
        self.path = ""

    def execute(self):
        if self.path == "":
            success = self.sys.change_directory("/")
        else:
            success = self.sys.change_directory(self.path)

        if not success:
            print(f"Failed to change directory to: {self.path}")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.path = ""

        for arg in s:
            if arg[0] != "-":
                self.path = arg
            else:
                print(f"Wrong argument: {arg}")
                return -1
        return 0


class LSCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-l", "-a"]
        self.passedArgs = []
        self.sys = sys
        self.path = ""

    def execute(self):
        self.sys.list_directory(self.path, self.passedArgs)

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

class VFS_SAVECommand(Command): # Команда для сохранения VFS
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys
        self.save_path = ""

    def execute(self):

        if self.save_path:
            success = self.sys.save_vfs(self.save_path)
            if success:
                print(f"VFS saved successfully to: {self.save_path}")
            else:
                print(f"Failed to save VFS to: {self.save_path}")
        else:
                print("Error: No save path specified")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.save_path = ""

        if len(s) == 0:
            print("Error: vfs-save requires a path argument")
            return -1

        if len(s) > 1:
            print("Error: vfs-save takes only one argument")
            return -1

        self.save_path = s[0]
        return 0