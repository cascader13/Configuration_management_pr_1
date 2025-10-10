import My_System
from Command import CDCommand, LSCommand, EXITCommand, WRONGCommand, VFS_SAVECommand, UNIQCommand, HEADCommand, CALCommand, RMCommand
import os


class CommandLine:
    def __init__(self, sys: My_System):
        try:
            self.sys = sys
            self.id = sys.User + "@" + sys.Comp + ":" + sys.current_path + "$"
            self.factory_command = {  # фабрика
                'cd': CDCommand(sys),
                'ls': LSCommand(sys),
                'exit': EXITCommand(sys),
                'vfs-save': VFS_SAVECommand(sys),
                'uniq': UNIQCommand(sys),
                'head': HEADCommand(sys),
                'cal': CALCommand(sys),
                'rm': RMCommand(sys),
                'wrong': WRONGCommand()
            }
            self.commands = ["cd", "ls", "exit", "vfs-save", "uniq", "head", "cal", "rm"]
        except Exception as e:
            print(f"Error initializing CommandLine: {e}")
            raise

    def update_prompt(self):
        self.id = self.sys.User + "@" + self.sys.Comp + ":" + self.sys.current_path + "$"

    def execute_script_command(self, command_line):
        try:
            s = command_line.split()
            if not s:
                return True

            command = s[0]
            args = []

            if command[0] == "$":
                value = os.getenv(command[1:])
                print(f"Value of '{command[1:]}' environment variable: {value}")
                return True

            if len(s) > 1:
                args = s[1:]

            if command not in self.commands:
                command_handler = self.factory_command["wrong"]
            else:
                command_handler = self.factory_command[command]

            if command_handler.ParseArgs(args) == -1:
                print("Error: Invalid arguments")
                return False
            else:
                command_handler.execute()
                self.update_prompt()
                return True

        except Exception as e:
            print(f"Error executing command '{command_line}': {e}")
            return False

    def execute(self):
        self.sys.is_running = True

        while self.sys.is_running:
            try:
                print(self.id, end=" ")
                user_input = input().strip()
                if not user_input:
                    continue

                s = user_input.split()
                command = s[0]
                args = []

                if command[0] == "$":
                    value = os.getenv(command[1:])
                    print(f"Value of '{command[1:]}' environment variable: {value}")
                    continue

                if len(s) > 1:
                    args = s[1:]

                if command not in self.commands:
                    command_handler = self.factory_command["wrong"]
                else:
                    command_handler = self.factory_command[command]

                if command_handler.ParseArgs(args) == -1:
                    print("Error: Invalid arguments")
                else:
                    command_handler.execute()
                    self.update_prompt()

            except KeyboardInterrupt:
                print("\nExiting...")
                self.sys.exit()
            except EOFError:
                print("\nExiting...")
                self.sys.exit()
            except Exception as e:
                print(f"Error: {e}")