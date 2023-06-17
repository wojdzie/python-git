import datetime
import os

from utils import find_repo_path


def run(args):
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