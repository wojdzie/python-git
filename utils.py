import os

REPO_DIR = ".pygit"


def find_repo_path():
    current_dir = os.getcwd()
    while current_dir != "/":
        repo_dir = os.path.join(current_dir, REPO_DIR)
        if os.path.exists(repo_dir):
            return repo_dir
        current_dir = os.path.dirname(current_dir)
    return None


def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return None
