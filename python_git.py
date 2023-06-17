import argparse
import os
import shutil
import datetime
import sys

import add
import init
from utils import find_repo_path


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

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    commit_id = f"{current_branch}_{timestamp}"
    commit_dir = os.path.join(commit_dir, current_branch, commit_id)
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
        raw_time = datetime.datetime.strptime(commit_id.split("_")[1], "%Y%m%d%H%M%S%f")
        timestamp = raw_time.strftime("%H:%M:%S.%f %d-%m-%Y")
        print(f"- Timestamp: {timestamp}, Branch: {branch}, Commit ID: {commit_id}")


def checkout(args):
    repo_path = find_repo_path()
    branch_dir = os.path.join(repo_path, "commits", args.branch)
    if not os.path.exists(branch_dir):
        current_branch_file = os.path.join(repo_path, "HEAD")
        current_branch = read_file(current_branch_file)

        os.makedirs(branch_dir)
        commit_dir = os.path.join(repo_path, "commits")
        current_commit = os.path.join(commit_dir, current_branch)
        shutil.copytree(current_commit, branch_dir, dirs_exist_ok=True)

    current_branch_file = os.path.join(repo_path, "HEAD")
    with open(current_branch_file, "w") as f:
        f.write(args.branch)

    print(f"Switched to branch '{args.branch}'.")
    update_working_directory(repo_path, args.branch)


def update_working_directory(repo_path, branch):
    parent_dir = os.path.dirname(repo_path)
    commit_dir = os.path.join(repo_path, "commits")
    branch_dir = os.path.join(commit_dir, branch)
    staging_dir = os.path.join(repo_path, "staging")

    for root, dirs, files in os.walk(parent_dir):
        if root == parent_dir:
            dirs[:] = [d for d in dirs if d != ".pygit"]
        for file in files:
            os.remove(os.path.join(root, file))

    if os.path.exists(staging_dir):
        for root, dirs, files in os.walk(staging_dir):
            for file in files:
                source_path = os.path.join(root, file)
                target_path = os.path.join(parent_dir, file)
                shutil.copy(source_path, target_path)

    if os.path.exists(branch_dir):
        files_to_copy = {}

        for root, dirs, files in os.walk(branch_dir):
            for file in files:
                source_path = os.path.join(root, file)
                timestamp = int(root.split("_")[-1])
                if file not in files_to_copy or timestamp > files_to_copy[file][0]:
                    files_to_copy[file] = (timestamp, source_path)

        for file, (timestamp, source_path) in files_to_copy.items():
            target_path = os.path.join(parent_dir, file)
            if not os.path.exists(target_path):
                shutil.copy(source_path, target_path)


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

    # Checkout command
    arg_sp_checkout = arg_subparsers.add_parser("checkout", help="Switch branches.")
    arg_sp_checkout.add_argument("branch", metavar="branch", help="Branch to switch to")

    args = arg_parser.parse_args(argv)

    if args.command == "init":
        init.run_init(args)
    elif args.command == "add":
        add.run_add(args)
    elif args.command == "commit":
        commit(args)
    elif args.command == "log":
        log(args)
    elif args.command == "checkout":
        checkout(args)


if __name__ == "__main__":
    main()
