import argparse
import io
import os
import shutil
import sys
import tempfile
import unittest

from python_git import init, add, commit, checkout


def _get_captured_output(func, args=None):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    if args is None:
        func()
    else:
        func(args)
    sys.stdout = sys.__stdout__
    return captured_output.getvalue().strip()


class GitClientTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".pygit")))

    def test_add(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)

        sample_file = os.path.join(self.temp_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("Sample content\n")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        staging_dir = os.path.join(self.temp_dir, ".pygit", "staging")
        staged_file = os.path.join(staging_dir, "sample.txt")
        self.assertTrue(os.path.exists(staged_file))

    def test_commit(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)

        sample_file = os.path.join(self.temp_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("Sample content\n")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        commit_dir = os.path.join(self.temp_dir, ".pygit", "commits")
        commit_ids = os.listdir(commit_dir)
        self.assertEqual(len(commit_ids), 1)

    def test_checkout_switch_branch(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)

        sample_file = os.path.join(self.temp_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("Sample content\n")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="develop")
        checkout(checkout_args)

        current_branch_file = os.path.join(self.temp_dir, ".pygit", "HEAD")
        with open(current_branch_file, "r") as f:
            current_branch = f.read().strip()

        self.assertEqual(current_branch, "develop")

    def test_checkout_updates_working_directory(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)

        sample_file = os.path.join(self.temp_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("Sample content\n")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="develop")
        checkout(checkout_args)

        sample_file2 = os.path.join(self.temp_dir, "sample2.txt")
        with open(sample_file2, "w") as f:
            f.write("Sample content 2\n")

        add_args = argparse.Namespace(files=[sample_file2])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="master")
        checkout(checkout_args)

        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "sample.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "sample2.txt")))

    def test_checkout_after_commits_should_reload_recent_version(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)

        sample_file = os.path.join(self.temp_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("Sample content\n")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="develop")
        checkout(checkout_args)

        with open(sample_file, "a") as f:
            f.write("Sample content 2\n")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="master")
        checkout(checkout_args)

        with open(sample_file, "r") as f:
            content = f.read()
            assert content.strip() == "Sample content"

        checkout_args = argparse.Namespace(branch="develop")
        checkout(checkout_args)

        with open(sample_file, "r") as f:
            lines = f.readlines()
            assert lines[0].strip() == "Sample content"
            assert lines[1].strip() == "Sample content 2"


if __name__ == "__main__":
    unittest.main()
