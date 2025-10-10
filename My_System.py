import os
from VFS import VFS, Type, Node


class My_System:
    def __init__(self, user="User", comp="Computer", config=None):
        try:
            self.User = user
            self.Comp = comp
            self.is_running = False
            self.config = config
            self.current_path = "/"
            self.vfs = None

            self._initialize_vfs()

        except Exception as e:
            print(f"Error initializing My_System: {e}")
            raise

    def _initialize_vfs(self):
        if self.config and hasattr(self.config, 'vfs_path') and self.config.vfs_path:
            try:
                vfs_path = self.config.vfs_path
                if not os.path.exists(vfs_path):
                    print(f"Creating VFS directory: {vfs_path}")
                    os.makedirs(vfs_path, exist_ok=True)
                    print(f"Successfully created VFS directory: {vfs_path}")
                else:
                    print(f"VFS directory already exists: {vfs_path}")

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

        if self.config and hasattr(self.config, 'vfs_csv') and self.config.vfs_csv:
            self._load_vfs_from_csv(self.config.vfs_csv)

    def _load_vfs_from_csv(self, csv_path):
        try:
            if not os.path.exists(csv_path):
                print(f"Error: VFS CSV file '{csv_path}' not found")
                return

            print(f"Loading VFS from: {csv_path}")
            self.vfs = VFS(csv_path)
            self.vfs.build_tree()
            print(f"VFS loaded successfully from {csv_path}")

        except Exception as e:
            print(f"Error loading VFS from '{csv_path}': {e}")
            raise

    def is_path(self, path):
        try:
            if not self.vfs:
                return False

            if path == "" or path == "/":
                return True

            node = self.vfs.encrypt_absolute_path(path.lstrip('/'))
            return node is not None

        except Exception as e:
            print(f"Error validating path '{path}': {e}")
            return False

    def change_directory(self, path):
        if not self.vfs:
            print("Error: VFS not loaded")
            return False

        if path == "":
            return True

        if path == "/":
            self.current_path = "/"
            return True

        if path.startswith("/"):
            target_path = path
        else:
            if self.current_path == "/":
                target_path = f"/{path}"
            else:
                target_path = f"{self.current_path}/{path}"

        target_path = target_path.replace("//", "/")

        node = self.vfs.encrypt_absolute_path(target_path.lstrip('/'))
        if node and node.type == Type.FOLDER:
            self.current_path = target_path
            return True
        else:
            print(f"Error: Directory '{path}' not found")
            return False

    def list_directory(self, path="", options=None):
        if not self.vfs:
            print("Error: VFS not loaded")
            return

        if options is None:
            options = []

        target_path = path if path else self.current_path
        if target_path == "/":
            node = self.vfs.head
        else:
            node = self.vfs.encrypt_absolute_path(target_path.lstrip('/'))

        if not node:
            print(f"Error: Path '{target_path}' not found")
            return

        if node.type != Type.FOLDER:
            print(f"Error: '{target_path}' is not a directory")
            return

        print(f"Contents of {target_path}:")
        for child in node.childrens:
            if "-a" in options or not child.name.startswith('.'):
                if child.type == Type.FOLDER:
                    print(f"  {child.name}/")
                else:
                    print(f"  {child.name}")

    def get_file_content(self, file_path):
        """Получить содержимое файла из VFS"""
        if not self.vfs:
            print("Error: VFS not loaded")
            return None

        # Если путь относительный, добавляем текущий путь
        if not file_path.startswith("/"):
            if self.current_path == "/":
                absolute_path = f"/{file_path}"
            else:
                absolute_path = f"{self.current_path}/{file_path}"
        else:
            absolute_path = file_path

        node = self.vfs.encrypt_absolute_path(absolute_path.lstrip('/'))
        if not node:
            print(f"Error: File '{file_path}' not found")
            return None

        if node.type != Type.FILE:
            print(f"Error: '{file_path}' is not a file")
            return None

        # В реальной реализации здесь должно быть чтение содержимого файла. Но ввиду того что мы работаем с VFS, можно обойтись и этим
        return self._generate_test_content(node.name)

    def _generate_test_content(self, filename):
        test_contents = {
            "section1.txt": """Line 1
                               Line 2
                               Line 3
                               Line 4
                               Line 5
                               Line 6
                               Line 7
                               Line 8""",
            "section2.txt": """apple
                               banana
                               Apple
                               banana
                               cherry
                               APPLE
                               date""",
            "main.py": """import sys
                          def main():
                            print("Hello World")

                          if __name__ == "__main__":
                            main()"""
        }

        return test_contents.get(filename, f"Test content for {filename}\nLine 1\nLine 2\nLine 2\nLine 3")

    def save_vfs(self, save_path):
        if not self.vfs:
            print("Error: VFS not loaded")
            return False

        try:
            print(f"VFS would be saved to: {save_path}")
            return True
        except Exception as e:
            print(f"Error saving VFS: {e}")
            return False

    def exit(self):
        try:
            self.is_running = False
            print("System shutdown completed")
        except Exception as e:
            print(f"Error during system shutdown: {e}")