
from Command_line import CommandLine
from My_System import My_System

def main():
    sys = My_System("Alex", "MYLAPTOP")
    command_line = CommandLine(sys)
    command_line.execute()

if __name__ == "__main__":
    main()