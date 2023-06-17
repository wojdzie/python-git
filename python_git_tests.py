import argparse
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

from python_git import init, add


def _get_captured_output(func):
    buffer = StringIO()
    with redirect_stdout(buffer):
        func()
    return buffer.getvalue().strip()


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


if __name__ == "__main__":
    unittest.main()
