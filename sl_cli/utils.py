#!/usr/bin/env python3
import json
import logging
import os
from sys import exit

from xdg import BaseDirectory

# XDG compliancy
CONFIG_DIR = f"{BaseDirectory.xdg_config_home}/sl-cli"
CONFIG_PATH = CONFIG_DIR + "/config.json"
LOG_PATH = f"{BaseDirectory.xdg_cache_home}/sl-cli.log"

# Logging
def logger():
    """Sets up logging at $XDG_CACHE_HOME/sl-cli.log"""

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w+") as log:
            pass

    logging.basicConfig(filename=LOG_PATH, encoding="utf-8", level=logging.DEBUG)


def retrieve_api_key():
    """Attempt loading api_key from $XDG_CONFIG_HOME/sl-cli/config.json"""
    try:
        with open(CONFIG_PATH) as config:
            api_key = json.load(config)["api_key"]

            return api_key

    except (json.decoder.JSONDecodeError, KeyError, FileNotFoundError) as e:
        logging.info(e)


def retrieve_api_url():
    """Attempt loading api_url from $XDG_CONFIG_HOME/sl-cli/config.json"""
    try:
        with open(CONFIG_PATH) as config:
            data = json.load(config)
            api_url = data["api_url"]

        return api_url

    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
        logging.info(e)
        api_url = "https://app.simplelogin.io"
        update_config({"api_url": api_url})

        return api_url


def mkdir_config():
    """Create the config directory named 'sl-cli' at $XDG_CONFIG_HOME/ if it isn't already created"""

    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)


def setup():
    """Wrapper function that start logging and returns the api_key and api_url"""
    logger()
    api_key = retrieve_api_key()

    if not api_key:
        print("Please login first by running 'sl-cli login'")
        exit(1)
    api_url = retrieve_api_url()

    return api_key, api_url


def update_config(key_val):
    """Update a key-value pair in the config file, by passing a dictionary"""
    data = {}

    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as config:
                data = json.load(config)
        except json.decoder.JSONDecodeError as e:
            logging.info(e)

    data.update(key_val)
    with open(CONFIG_PATH, "w") as config:
        json.dump(data, config)


def check_error(response, error_msg="Error"):
    """Checks if response returned an error and if it did, exits with an error message, after logging the response"""

    if response.status_code // 10 != 20:
        print(error_msg)
        logging.info(response.text)
        exit(1)


mkdir_config()
