import argparse
import sys

import add
import checkout
import commit
import init
import log

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


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = arg_parser.parse_args(argv)

    if args.command == "init":
        init.run_init(args)
    elif args.command == "add":
        add.run_add(args)
    elif args.command == "commit":
        commit.run_commit(args)
    elif args.command == "log":
        log.run_log(args)
    elif args.command == "checkout":
        checkout.run_checkout(args)


if __name__ == "__main__":
    main()
