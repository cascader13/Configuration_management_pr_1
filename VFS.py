import os
import re
import shlex
import argparse


class VFS:
    def __init__(self):
        self.currentpath = ""
        self.name = "VFS"
    def process(self):
        while True:
            cmd = input(f'{self.name}:{self.currentpath}\$').split(" ")
            if cmd[0] == "exit":
                self.exit()
            elif cmd[0] == "ls":
                try:
                    if not self.ls(cmd[1]):
                        print(f'Directory "{cmd[1]}" if not exist.')
                except:
                    self.cd("")
            elif cmd[0] == "cd":
                try:
                    if not self.cd(cmd[1]):
                        print(f'Directory "{cmd[1]}" not exist.')
                except:
                    self.cd("")
            elif cmd[0][0] == '$':
                self.local_variables(cmd[0][1::])
            else:
                print("unknown command")

    def local_variables(self, name: str):
        print("I local variable", name)
    def ls(self, path: str):
        print("i ls")

    def cd(self, path: str):
        print("i cd")

    def exit(self):
        exit(0)


def main():
    vfs = VFS()
    vfs.process()


if __name__ == '__main__':
    main()
