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
            f.write("Sample content")

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
            f.write("Sample content")

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
            f.write("Sample content")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="branch1")
        checkout(checkout_args)

        current_branch_file = os.path.join(self.temp_dir, ".pygit", "HEAD")
        with open(current_branch_file, "r") as f:
            current_branch = f.read().strip()

        self.assertEqual(current_branch, "branch1")

    def test_checkout_updates_working_directory(self):
        init_args = argparse.Namespace(path=self.temp_dir)
        init(init_args)

        sample_file = os.path.join(self.temp_dir, "sample.txt")
        with open(sample_file, "w") as f:
            f.write("Sample content")

        add_args = argparse.Namespace(files=[sample_file])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="branch1")
        checkout(checkout_args)

        sample_file2 = os.path.join(self.temp_dir, "sample2.txt")
        with open(sample_file2, "w") as f:
            f.write("Sample content 2")

        add_args = argparse.Namespace(files=[sample_file2])
        add(add_args)

        commit_args = argparse.Namespace()
        commit(commit_args)

        checkout_args = argparse.Namespace(branch="master")
        checkout(checkout_args)

        # Check if the file exists in the working directory
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "sample.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "sample2.txt")))


if __name__ == "__main__":
    unittest.main()
