import os
import shutil

from utils import find_repo_path


def run(args):
    repo_path = find_repo_path()
    staging_dir = os.path.join(repo_path, "staging")

    for file_path in args.files:
        if os.path.exists(file_path):
            shutil.copy(file_path, staging_dir)
            print(f"Added '{file_path}' to the staging area.")
        else:
            print(f"Skipping '{file_path}' - File does not exist.")