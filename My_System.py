import os


class My_System:
    def __init__(self, user="User", comp="Computer", config=None):
        try:
            self.User = user
            self.Comp = comp
            self.is_running = False
            self.config = config

            self._initialize_vfs()

        except Exception as e:
            print(f"Error initializing My_System: {e}")
            raise

    def _initialize_vfs(self):
        """Initialize VFS directory with proper error handling"""
        if self.config and hasattr(self.config, 'vfs_path') and self.config.vfs_path:
            try:
                vfs_path = self.config.vfs_path
                if not os.path.exists(vfs_path):
                    print(f"Creating VFS directory: {vfs_path}")
                    os.makedirs(vfs_path, exist_ok=True)
                    print(f"Successfully created VFS directory: {vfs_path}")
                else:
                    print(f"VFS directory already exists: {vfs_path}")

                # Verify we can write to the directory
                test_file = os.path.join(vfs_path, "test_write.tmp")
                try:
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                except Exception as e:
                    print(f"Warning: Cannot write to VFS directory '{vfs_path}': {e}")

            except PermissionError as e:
                print(f"Error: No permission to create VFS directory '{vfs_path}': {e}")
                raise
            except Exception as e:
                print(f"Error creating VFS directory '{vfs_path}': {e}")
                raise

    def is_path(self, path):
        try:
            if len(path) == 0 or path[0] == "/":
                return True
            return False
        except Exception as e:
            print(f"Error validating path '{path}': {e}")
            return False

    def exit(self):
        try:
            self.is_running = False
            print("System shutdown completed")
        except Exception as e:
            print(f"Error during system shutdown: {e}")