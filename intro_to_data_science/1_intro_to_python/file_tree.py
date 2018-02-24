""" Implementation of file tree by os.walk. Start drawin' on current directory"""
import os


def file_tree(path, file_filter=None):
    basic_intent = "\t"
    if path.endswith(os.sep):
        path = path[:-1]
    if os.path.isfile(path):
        print(path)
    for root, _, files in os.walk(path):
        level = root[len(path):].count(os.sep)
        intent = basic_intent * level
        print("{0}{1}:".format(intent, os.path.basename(root)))
        file_intent = basic_intent * (level + 1)
        for file_name in files:
            if file_filter is not None and not file_name.endswith(file_filter):
                continue
            print("{0}{1}".format(file_intent, file_name))


if __name__ == '__main__':
    file_tree(".", "json")
