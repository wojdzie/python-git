import argparse
import os
import shutil
import datetime
import sys

REPO_DIR = ".pygit"


def init(args):
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


def commit(args):
    repo_path = find_repo_path()

    staging_dir = os.path.join(repo_path, "staging")
    commit_dir = os.path.join(repo_path, "commits")
    current_branch_file = os.path.join(repo_path, "HEAD")

    current_branch = read_file(current_branch_file)
    if current_branch is None:
        print("No branch is currently checked out.")
        return

    if len(os.listdir(staging_dir)) == 0:
        print("No changes added to commit.")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    commit_id = f"{current_branch}_{timestamp}"
    commit_dir = os.path.join(commit_dir, commit_id)
    os.makedirs(commit_dir)

    for file_name in os.listdir(staging_dir):
        file_path = os.path.join(staging_dir, file_name)
        target_path = os.path.join(commit_dir, file_name)
        shutil.copy(file_path, target_path)
        os.remove(file_path)

    shutil.rmtree(staging_dir)
    os.makedirs(staging_dir)

    print(f"Committed changes to branch '{current_branch}' with commit ID: {commit_id}.")


def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return None


def log(args):
    repo_path = find_repo_path()
    if repo_path is None:
        print("Not a git repository.")
        return

    commit_dir = os.path.join(repo_path, "commits")

    print("Commit history:")
    for commit_id in os.listdir(commit_dir):
        branch = commit_id.split("_")[0]
        timestamp = commit_id.split("_")[1]
        print(f"- Branch: {branch}, Timestamp: {timestamp}, Commit ID: {commit_id}")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    arg_parser = argparse.ArgumentParser()
    arg_subparsers = arg_parser.add_subparsers(title="Commands", dest="command")
    arg_subparsers.required = True

    # Init command
    arg_sp_init = arg_subparsers.add_parser("init", help="Initialize a new, empty repository.")
    arg_sp_init.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repository")

    # Add command
    arg_sp_add = arg_subparsers.add_parser("add", help="Add file(s) to the staging area.")
    arg_sp_add.add_argument("files", metavar="file", nargs="+", help="File(s) to add")

    # Commit command
    arg_sp_commit = arg_subparsers.add_parser("commit", help="Create a commit from staged changes")

    # Log command
    arg_sp_log = arg_subparsers.add_parser("log", help="Display commit history for the repository.")

    args = arg_parser.parse_args(argv)

    if args.command == "init":
        init(args)
    elif args.command == "add":
        add(args)
    elif args.command == "commit":
        commit(args)
    elif args.command == "log":
        log(args)


if __name__ == "__main__":
    main()

