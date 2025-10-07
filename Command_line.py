import My_System
from Command import CDCommand, LSCommand, EXITCommand, WRONGCommand
import os


class CommandLine:
    def __init__(self, sys: My_System):
        try:
            self.sys = sys
            self.id = sys.User + "@" + sys.Comp + ":"
            self.factory_command = {
                'cd': CDCommand(sys),
                'ls': LSCommand(sys),
                'exit': EXITCommand(sys),
                'wrong': WRONGCommand()
            }
            self.commands = ["cd", "ls", "exit"]
        except Exception as e:
            print(f"Error initializing CommandLine: {e}")
            raise

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

            except KeyboardInterrupt:
                print("\nExiting...")
                self.sys.exit()
            except EOFError:
                print("\nExiting...")
                self.sys.exit()
            except Exception as e:
                print(f"Error: {e}")