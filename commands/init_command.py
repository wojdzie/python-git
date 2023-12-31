import os

from utils import REPO_DIR


def run(args):
    repo_path = os.path.abspath(args.path)
    pygit_dir = os.path.join(repo_path, REPO_DIR)

    if os.path.exists(pygit_dir):
        print("Repository already exists.")
        return

    os.makedirs(pygit_dir, exist_ok=True)

    staging_dir = os.path.join(pygit_dir, "staging")
    os.makedirs(staging_dir, exist_ok=True)

    commits_dir = os.path.join(pygit_dir, "commits")
    os.makedirs(commits_dir, exist_ok=True)

    head_file = os.path.join(pygit_dir, "HEAD")
    with open(head_file, "w") as f:
        f.write("master")

    print(f"Initialized empty PyGit repository in {repo_path}/.pygit")