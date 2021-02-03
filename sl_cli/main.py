#!/usr/bin/env python3

import argparse

from . import login
from . import utils
from . import aliases


def main():

    # Setup arguments
    parser = argparse.ArgumentParser(description="SimpleLogin CLI application")
    subparser = parser.add_subparsers(dest="command")
    login = subparser.add_parser("login", help="Login into your SimpleLogin account")
    ls = subparser.add_parser("ls", help="List your aliases")
    new = subparser.add_parser("new", help="Add a new alias")
    new_random = subparser.add_parser("new_random", help="Add a new random alias")
    rm = subparser.add_parser("rm", help="Remove an alias")
    args = parser.parse_args()

    if args.command == "login":
        login.login()

    elif args.command == "ls":
        Aliases = aliases.get_aliases()

        for Alias in Aliases:
            print(Alias)

    elif args.command == "new":
        aliases.new_alias()

    elif args.command == "new_random":
        aliases.new_random_alias()

    elif args.command == "rm":
        aliases.delete_alias()


if __name__ == "__main__":
    main()
