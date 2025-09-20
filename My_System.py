

class My_System:
    def __init__(self, user, comp):
        self.User = user
        self.Comp = comp
        self.is_running = False

    def is_path(self, path):
        if len(path) == 0 or path[0] == "/":
            return True
        return False

    def exit(self):
        self.is_running = False