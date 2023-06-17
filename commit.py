import datetime
import os
import shutil

from utils import find_repo_path, read_file


def run_commit(args):
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