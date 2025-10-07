import argparse
import toml
import os
import sys


class Config:
    def __init__(self):
        self.vfs_path = None
        self.startup_script = None
        self.config_file = None

        try:
            self._parse_arguments()
            self._load_config_file()
            self._print_config()
        except Exception as e:
            print(f"Configuration error: {e}")
            sys.exit(1)

    def _parse_arguments(self):
        try:
            parser = argparse.ArgumentParser(description='File system emulator')

            parser.add_argument('--vfs-path',
                                help='Path to VFS')
            parser.add_argument('--startup-script',
                                help='Path to startup script')
            parser.add_argument('--config-file',
                                default='config.toml',
                                help='Path to config file (default: config.toml)')

            args = parser.parse_args()

            self.vfs_path = args.vfs_path
            self.startup_script = args.startup_script
            self.config_file = args.config_file

        except argparse.ArgumentError as e:
            print(f"Argument parsing error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during argument parsing: {e}")
            raise

    def _load_config_file(self):
        try:
            if self.config_file and os.path.exists(self.config_file):
                print(f"Loading configuration from: {self.config_file}")
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = toml.load(f)

                # Load values from file only if not set in command line
                if not self.vfs_path and 'vfs_path' in config_data:
                    self.vfs_path = config_data['vfs_path']
                    print(f"Loaded vfs_path from config: {self.vfs_path}")

                if not self.startup_script and 'startup_script' in config_data:
                    self.startup_script = config_data['startup_script']
                    print(f"Loaded startup_script from config: {self.startup_script}")

            elif self.config_file:
                print(f"Warning: Config file '{self.config_file}' not found, using command line arguments only")

        except toml.TomlDecodeError as e:
            print(f"Error: Invalid TOML format in config file '{self.config_file}': {e}")
            raise
        except PermissionError as e:
            print(f"Error: No permission to read config file '{self.config_file}': {e}")
            raise
        except Exception as e:
            print(f"Error reading config file '{self.config_file}': {e}")
            raise

    def _print_config(self):
        print("=== Emulator Configuration ===")
        print(f"VFS Path: {self.vfs_path or 'Not set'}")
        print(f"Startup Script: {self.startup_script or 'Not set'}")
        print(f"Config File: {self.config_file or 'Not set'}")
        print("==============================")