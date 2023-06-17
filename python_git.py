import os
import shutil

REPO_DIR = ".pygit"


def init(args):
    repo_path = os.path.abspath(args.path)
    pygit_dir = os.path.join(repo_path, REPO_DIR)

    if os.path.exists(pygit_dir):
        print("Repository already exists.")
        return

    os.makedirs(pygit_dir, exist_ok=True)
    print(f"Initialized empty repository in {pygit_dir}")

    staging_dir = os.path.join(pygit_dir, "staging")
    os.makedirs(staging_dir, exist_ok=True)

    commits_dir = os.path.join(pygit_dir, "commits")
    os.makedirs(commits_dir, exist_ok=True)

    head_file = os.path.join(pygit_dir, "HEAD")
    with open(head_file, "w") as f:
        f.write("master")

    print(f"Initialized empty PyGit repository in {repo_path}/.pygit")


def add(args):
    repo_path = find_repo_path()
    staging_dir = os.path.join(repo_path, "staging")

    for file_path in args.files:
        if os.path.exists(file_path):
            shutil.copy(file_path, staging_dir)
            print(f"Added '{file_path}' to the staging area.")
        else:
            print(f"Skipping '{file_path}' - File does not exist.")


def find_repo_path():
    current_dir = os.getcwd()
    while current_dir != "/":
        repo_dir = os.path.join(current_dir, REPO_DIR)
        if os.path.exists(repo_dir):
            return repo_dir
        current_dir = os.path.dirname(current_dir)
    return None
