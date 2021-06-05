#!/usr/bin/env python3

import requests

from . import mailboxes
from . import utils


def get_aliases():
    """Return a list of Aliases"""

    API_KEY, API_URL = utils.setup()
    Aliases = []
    headers = {"Authentication": API_KEY}
    i = 0
    while True:
        params = {"page_id": i}

        r = requests.get(url=API_URL + "/api/v2/aliases", params=params, headers=headers)

        utils.check_error(r, "Error fetching aliases")
        aliases = r.json()["aliases"]

        for alias in aliases:
            Aliases.append(Alias(alias))
        if len(aliases) != 20:
            break
        i = i + 1

    return Aliases


def alias_options():
    """Return available alias suffixes, used for a creating a new alias"""

    API_KEY, API_URL = utils.setup()
    headers = {"Authentication": API_KEY}
    r = requests.get(url=API_URL + "/api/v5/alias/options", headers=headers)
    utils.check_error(r, "Error fetching suffixes")
    suffixes = r.json()["suffixes"]

    return suffixes


def new_alias():
    """Create a new alias"""

    API_KEY, API_URL = utils.setup()
    prefix = input("Enter alias prefix: ")
    name = input("Enter alias name (optional): ")
    note = input("Enter alias note (optional): ")

    suffixes = alias_options()

    print()

    for n, suffix in enumerate(suffixes):
        print(f"{n+1} ", suffix["suffix"])

    choice = input(
        f"Choose one of the following prefixes[{suffixes[0]['signed_suffix']}]: "
    )

    if choice == "":
        choice = 1
    else:
        choice = int(choice)

    signed_suffix = suffixes[choice - 1]["signed_suffix"]

    print()
    mailboxes = mailboxes.get_mailboxes()["mailboxes"]

    for n, box in enumerate(mailboxes):
        print(f"{n+1}", f"{box['email']}")
    email = input(f"Choose one of the following emails[{mailboxes[0]['email']}]")

    if email == "":
        email = 1

    email = int(email)
    email = mailboxes[email - 1]["id"]

    print()
    print(f"Creating new alias {prefix+suffixes[choice-1]['suffix']}")

    if name != "":
        print(f"Name: {name}")

    if note != "":
        print(f"Note: {note}")
    print(f"Recipient: {email}")

    headers = {"Authentication": API_KEY}
    payload = {
        "alias_prefix": prefix,
        "signed_suffix": signed_suffix,
        "mailbox_ids": [email],
        "note": note,
        "name": name,
    }

    r = requests.post(
        API_URL + "/api/v3/alias/custom/new", headers=headers, json=payload
    )
    utils.check_error(r, "Error creating a new alias")


def delete_alias(name=""):
    """Delete an alias"""

    API_KEY, API_URL = utils.setup()

    if name != "":
        alias = name

        alias_id = ""
        Aliases = get_aliases()

        for Alias in Aliases:
            if alias == Alias.__str__() and alias_id == "":
                alias_id = Alias.id

        if alias_id == "":
            print("No such alias")
            exit(1)

    else:
        Aliases = get_aliases()

        for n, alias in enumerate(Aliases):
            print(n + 1, alias)

        alias = int(input("Choose an alias to delete: "))
        alias = Aliases[alias - 1]
        alias_id = alias.id

    print()
    print(alias)
    confirm = input("Are you absolutely sure you want to delete this alias?(YES, NO) ")

    if confirm == "YES":
        headers = {"Authentication": API_KEY}
        params = {"alias_id": alias_id}
        r = requests.delete(
            API_URL + f"/api/aliases/{alias_id}", params=params, headers=headers
        )
        utils.check_error(r, "Error deleting alias")
        print("Deleted alias")
    else:
        print("Exiting...")


def new_random_alias():
    """Create a new random alias"""

    API_KEY, API_URL = utils.setup()
    headers = {"Authentication": API_KEY}

    note = input("Enter alias note (optional): ")
    payload = {
        "note": note,
    }
    print("Creating new random alias...")
    r = requests.post(API_URL + "/api/alias/random/new", headers=headers, json=payload)
    utils.check_error(r, "Error fetching suffixes")
    alias = r.json()["alias"]
    print("Created", alias)


class Alias(dict):
    def __init__(self, dict):
        self.creation_date = dict["creation_date"]
        self.email = dict["email"]
        self.id = dict["id"]

    def __str__(self):
        return f"{self.email}"


if __name__ == "__main__":
    get_aliases()
