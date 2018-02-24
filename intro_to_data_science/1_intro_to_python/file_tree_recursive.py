""" Recursive implementation of file tree"""
import os

DEFAULT_INTENT = "\t"


def file_tree_recursive(path, level, file_filter=None):
    for file_name in os.listdir(path):
        full_file_name = os.path.join(path, file_name)
        if os.path.isfile(full_file_name):
            if file_filter is not None and not file_name.endswith(file_filter):
                continue
            print("{0}{1}".format(DEFAULT_INTENT * level, file_name))
        elif os.path.isdir(full_file_name):
            print("{0}{1}:".format(DEFAULT_INTENT * level, file_name))
            file_tree_recursive(full_file_name, level + 1, file_filter)


def file_tree(path, file_filter=None):
    if os.path.isfile(path):
        print(path)
        return
    file_tree_recursive(path, 0, file_filter)


if __name__ == "__main__":
    file_tree(".", "json")
