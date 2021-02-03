#!/usr/bin/env python3

import argparse

from .login import login
from .utils import logger
from .aliases import (
    alias_options,
    delete_alias,
    get_aliases,
    new_alias,
    new_random_alias,
)


def main():

    # Setup arguments
    parser = argparse.ArgumentParser(description="SimpleLogin CLI application")
    parser.add_argument(
        "command",
        help="""One of the following: login list-aliases alias-options new-alias delete-alias new-random-alias""",
    )

    args = parser.parse_args()
    if args.command == "login":
        login()

    elif args.command == "list-aliases":
        aliases = get_aliases()

        for alias in aliases:
            print(alias)

    elif args.command == "alias-options":
        alias_options()

    elif args.command == "new-alias":
        new_alias()

    elif args.command == "delete-alias":
        delete_alias()

    elif args.command == "new-random-alias":
        new_random_alias()

    else:
        print(f"Unrecognized command: {args.command}")
