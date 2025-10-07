from Command_line import CommandLine
from My_System import My_System
from Configuration import Config
import sys
import traceback
import os


def main():
    try:
        print("=== Starting File System Emulator ===")

        config = Config()
        sys_obj = My_System("Alex", "MYLAPTOP", config)
        if config.startup_script:
            execute_startup_script(sys_obj, config.startup_script)

        start_interactive_mode(sys_obj)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("=== Emulator stopped ===")


def execute_startup_script(sys_obj, script_path):
    try:
        print(f"=== Executing startup script: {script_path} ===")

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Startup script '{script_path}' not found")

        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        command_line = CommandLine(sys_obj)
        script_success = True

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            print(f"{command_line.id} {line}")
            try:
                result = command_line.execute_script_command(line)
                if not result:
                    print(f"Error at line {line_num}: script execution interrupted")
                    script_success = False
                    break
            except Exception as e:
                print(f"Error executing line {line_num}: {e}")
                script_success = False
                break

        if script_success:
            print("=== Startup script completed successfully ===")
        else:
            print("=== Startup script execution failed ===")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print(f"Error: No permission to read startup script '{script_path}': {e}")
    except Exception as e:
        print(f"Error executing startup script '{script_path}': {e}")
        raise


def start_interactive_mode(sys_obj):
    print("\n=== Starting interactive mode ===")
    print("Available commands: cd, ls, exit")
    print("Example: ls -l /home")
    print("Press Ctrl+C to exit\n")

    try:
        command_line = CommandLine(sys_obj)
        command_line.execute()
    except KeyboardInterrupt:
        print("\nInteractive mode interrupted by user")
    except Exception as e:
        print(f"Error in interactive mode: {e}")
        raise


if __name__ == "__main__":
    main()