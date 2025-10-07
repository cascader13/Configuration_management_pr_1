
from enum import Enum
import csv

class Type(Enum):
    FOLDER = 1
    FILE = 2
    NONE = 3

class Node:

    def __init__(self, name: str, type : Type, parent=None):
        self.name = ""
        self.type = type
        self.parent = parent
        self.childrens = list()

    def add(self, children):
        self.childrens.append(children)

    def remove(self):
        for children in self.childrens:
            children.remove()
        del self

    def get(self, name):
        for children in self.childrens:
            if children.name == name:
                return children
        return Node("..", Type.NONE)

    def path_node(self):
        path = ""
        if self.parent != None:
            path = self.parent.print_node() + "/"
        return path + self.name


class VFS:

    def __init__(self, path):
        self.path = path
        self.head = Node("..", Type.NONE)

    def add(self, name, type, parent : Node):
        children = Node(name, type, parent)
        parent.add(children)

    def type_of_node(self, name):
        if '.' in name:
            return Type.FILE
        else:
            return Type.FOLDER

    def encrypt_absolute_path(self, absolute_path):
        path = absolute_path.split("/")
        current = self.head
        for node in path:
            current = current.get(node.name)
            if current.name == self.head.name:
                print(f"ERROR: path {absolute_path} not exist")
                return self.head
        return current

    def create_node(self, absolute_path:str):
        path = absolute_path.split("/")
        name = path[-1]
        path.pop(-1)
        current = self.head
        for node in path:
            current = current.get(node.name)
        type = self.type_of_node(name)
        self.add(name, type, current)

    def build_tree(self):
        with open('sw_data.csv') as f:
            reader = csv.reader(f)
            for absolute_path in reader:
                self.create_node(absolute_path)


