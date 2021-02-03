#!/usr/bin/env python3

import logging
import sys
from getpass import getpass
from sys import exit

import requests

from .utils import logger, retrieve_api_key, retrieve_api_url, update_config

api_url = retrieve_api_url()

# Logging
logger()


def login():
    """Login"""

    init_config = True
    api_key = retrieve_api_key()

    if api_key:
        login_again = input("It apppears you have already logged in, login again?[yn] ")

        if login_again.lower()[0] != "y":
            print("Exiting...")
            exit(0)

    if init_config:
        email = input("Enter your email: ")
        password = getpass("Enter your password: ")

        logging.info("Initializing config")

        payload = {
            "email": f"{email}",
            "password": f"{password}",
            "device": "Arch Linux",
        }

        r = requests.post(
            url=api_url + "/api/auth/login",
            json=payload,
        )

        try:
            response = r.json()
            api_key = response["api_key"]
            # Update
            update_config({"api_key": api_key})
            logging.info("Succesfully logged in")
            print("Succesfully logged in")

        except (KeyError, Exception) as e:
            logging.error(e)
            print("Check your username and password and try again", file=sys.stderr)
            exit(1)


if __name__ == "__main__":
    login()
