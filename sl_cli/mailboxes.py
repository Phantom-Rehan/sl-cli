#!/usr/bin/env python3

import requests

from .utils import check_error, setup


def get_mailboxes():
    """Return mailboxes"""

    API_KEY, API_URL = setup()
    headers = {"Authentication": API_KEY}
    r = requests.get(url=API_URL + "/api/v2/mailboxes", headers=headers)
    check_error(r, "Error fetching mailboxes")

    return r.json()


if __name__ == "__main__":
    get_mailboxes()
