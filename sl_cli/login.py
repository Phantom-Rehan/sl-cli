#!/usr/bin/env python3

import logging
import sys
from getpass import getpass
from sys import exit

import requests

from . import utils


def login():
    """Login"""

    # Logging
    utils.logger()

    init_config = True
    API_KEY = utils.retrieve_api_key()
    API_URL = utils.retrieve_api_url()

    if API_KEY:
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
            url=API_URL + "/api/auth/login",
            json=payload,
        )

        try:
            response = r.json()
            API_KEY = response["api_key"]
            # Update
            utils.update_config({"api_key": API_KEY})
            logging.info("Succesfully logged in")
            print("Succesfully logged in")

        except (KeyError, Exception) as e:
            logging.error(e)
            print("Check your username and password and try again", file=sys.stderr)
            exit(1)


if __name__ == "__main__":
    login()
