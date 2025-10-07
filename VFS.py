from enum import Enum
import csv


class Type(Enum):
    FOLDER = 1
    FILE = 2
    NONE = 3


class Node:

    def __init__(self, name: str, type: Type, parent=None):
        self.name = name
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
        return None

    def path_node(self):
        path = ""
        if self.parent != None:
            path = self.parent.path_node() + "/"
        return path + self.name


class VFS:

    def __init__(self, path):
        self.path = path
        self.head = Node("", Type.FOLDER)

    def add(self, name, type, parent: Node):
        children = Node(name, type, parent)
        parent.add(children)
        print(f"Added: {children.path_node()}")
        print(f"Parent: {parent.name}")
        print(f"Child: {children.name}")

    def type_of_node(self, name):
        if '.' in name:
            return Type.FILE
        else:
            return Type.FOLDER

    def encrypt_absolute_path(self, absolute_path):
        path = absolute_path.split("/")
        current = self.head
        for node_name in path:
            if node_name == "":
                continue
            current = current.get(node_name)
            if current is None:
                print(f"ERROR: path {absolute_path} not exist")
                return None
        return current

    def create_node(self, absolute_path: str):
        path = absolute_path.split("/")
        path = [p for p in path if p != ""]

        if not path:
            return

        name = path[-1]
        parent_path = path[:-1]

        current = self.head
        for node_name in parent_path:
            next_node = current.get(node_name)
            if next_node is None:
                next_node = Node(node_name, Type.FOLDER, current)
                current.add(next_node)
            current = next_node

        type = self.type_of_node(name)
        self.add(name, type, current)

    def build_tree(self):
        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    self.create_node(row[0])