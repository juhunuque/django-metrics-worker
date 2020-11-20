import os
import diffing


def get_assets_folder():
    return os.path.join(os.path.abspath(os.path.dirname(diffing.__file__)), 'assets')


def is_file_exists(path):
    return os.path.exists(path)


def remove_file(path):
    if is_file_exists(path):
        os.remove(path)
        return path
    return False
