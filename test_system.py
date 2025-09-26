# test_system.py
import pytest
import os
from unittest.mock import patch
from io import StringIO
import sys

from My_System import My_System
from Command_line import CommandLine
from Command import CDCommand, LSCommand, EXITCommand, WRONGCommand


class TestMySystem:

    def test_initialization(self):
        system = My_System("Alex", "MYLAPTOP")
        assert system.User == "Alex"
        assert system.Comp == "MYLAPTOP"
        assert system.is_running == False

    def test_is_path(self):
        system = My_System("Alex", "MYLAPTOP")
        assert system.is_path("/home/user") == True
        assert system.is_path("/") == True
        assert system.is_path("") == True

        assert system.is_path("home/user") == False
        assert system.is_path("relative/path") == False

    def test_exit(self):
        system = My_System("Alex", "MYLAPTOP")
        system.is_running = True
        system.exit()
        assert system.is_running == False


class TestCommands:

    def setup_method(self):
        self.system = My_System("Alex", "MYLAPTOP")

    def test_cd_command_initialization(self):
        cd_cmd = CDCommand(self.system)
        assert cd_cmd.validArgs == ["-c", "-d"]
        assert cd_cmd.passedArgs == []
        assert cd_cmd.path == ""
        assert cd_cmd.sys == self.system

    def test_cd_command_parse_args(self):
        cd_cmd = CDCommand(self.system)

        result = cd_cmd.ParseArgs(["/home/user", "-c", "-d"])
        assert result == 0
        assert cd_cmd.path == "/home/user"
        assert cd_cmd.passedArgs == ["-c", "-d"]

        cd_cmd = CDCommand(self.system)
        result = cd_cmd.ParseArgs(["/home"])
        assert result == 0
        assert cd_cmd.path == "/home"
        assert cd_cmd.passedArgs == []

        cd_cmd = CDCommand(self.system)
        result = cd_cmd.ParseArgs(["/home", "-invalid"])
        assert result == -1

    def test_cd_command_execute(self, capsys):
        cd_cmd = CDCommand(self.system)

        cd_cmd.path = "/home/user"
        cd_cmd.passedArgs = ["-c"]
        cd_cmd.execute()

        captured = capsys.readouterr()
        assert "i am ls" in captured.out
        assert "path is Correct" in captured.out
        assert "Arguments ['-c']" in captured.out

        cd_cmd.path = "home/user"
        cd_cmd.execute()

        captured = capsys.readouterr()
        assert "path is Uncorrect" in captured.out

    def test_ls_command_initialization(self):
        ls_cmd = LSCommand(self.system)
        assert ls_cmd.validArgs == ["-l", "-s"]
        assert ls_cmd.passedArgs == []
        assert ls_cmd.path == ""
        assert ls_cmd.sys == self.system

    def test_ls_command_parse_args(self):
        ls_cmd = LSCommand(self.system)

        result = ls_cmd.ParseArgs(["/home/user", "-l", "-s"])
        assert result == 0
        assert ls_cmd.path == "/home/user"
        assert ls_cmd.passedArgs == ["-l", "-s"]

        ls_cmd = LSCommand(self.system)
        result = ls_cmd.ParseArgs(["/home", "-invalid"])
        assert result == -1

    def test_exit_command(self):
        exit_cmd = EXITCommand(self.system)

        assert exit_cmd.ParseArgs([]) == 0
        assert exit_cmd.ParseArgs(["arg"]) == -1

        self.system.is_running = True
        exit_cmd.execute()
        assert self.system.is_running == False

    def test_wrong_command(self, capsys):
        wrong_cmd = WRONGCommand()
        assert wrong_cmd.ParseArgs(["any", "args"]) == 0
        wrong_cmd.execute()
        captured = capsys.readouterr()
        assert "Wrong command" in captured.out


class TestCommandLine:

    def setup_method(self):
        self.system = My_System("Alex", "MYLAPTOP")
        self.command_line = CommandLine(self.system)

    def test_initialization(self):
        assert self.command_line.sys == self.system
        assert self.command_line.id == "Alex@MYLAPTOP:"
        assert "cd" in self.command_line.factory_command
        assert "ls" in self.command_line.factory_command
        assert "exit" in self.command_line.factory_command
        assert "wrong" in self.command_line.factory_command
        assert self.command_line.commands == ["cd", "ls", "exit"]

    @patch('builtins.input', side_effect=['exit'])
    def test_execute_exit_command(self, mock_input, capsys):
        self.command_line.execute()
        assert self.system.is_running == False

    @patch('builtins.input', side_effect=['unknown_command', 'exit'])
    def test_execute_unknown_command(self, mock_input, capsys):
        self.command_line.execute()

        captured = capsys.readouterr()
        assert "Wrong command" in captured.out

    @patch('builtins.input', side_effect=['cd /home/user -c', 'exit'])
    def test_execute_cd_command(self, mock_input, capsys):
        self.command_line.execute()

        captured = capsys.readouterr()
        assert "i am ls" in captured.out
        assert "path is Correct" in captured.out
        assert "Arguments ['-c']" in captured.out

    @patch('builtins.input', side_effect=['ls /home -l', 'exit'])
    def test_execute_ls_command(self, mock_input, capsys):
        self.command_line.execute()

        captured = capsys.readouterr()
        assert "i am ls" in captured.out
        assert "path is Correct" in captured.out
        assert "Arguments ['-l']" in captured.out

    @patch('builtins.input', side_effect=['cd -invalid_args', 'exit'])
    def test_execute_invalid_args(self, mock_input, capsys):
        self.command_line.execute()
        captured = capsys.readouterr()
        assert "wrong arguments" in captured.out

    @patch('builtins.input', side_effect=['$HOME', 'exit'])
    @patch.dict(os.environ, {'HOME': '/home/user'})
    def test_environment_variable(self, mock_input, capsys):
        self.command_line.execute()
        captured = capsys.readouterr()
        assert "Value of 'HOME' environment variable" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])