import logging
import os
import sys

import click as click
import yaml

from notion_gcal_sync.clients.GCalClient import GCalClient
from notion_gcal_sync.config import Config

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".notion-gcal-sync")
CONFIG_FILE = os.path.join(CONFIG_PATH, "config.yml")
CONFIG_DEFAULT_FILE = os.path.join(CONFIG_PATH, "config.default.yml")
TOKEN_FILE = os.path.join(CONFIG_PATH, "token.json")
CREDENTIALS_FILE = os.path.join(CONFIG_PATH, "client_credentials.json")


def confirm_path(path):
    logging.info("{} does not exist".format(path))
    if click.confirm("Create non-existing {}?".format(path), default=True):
        return
    logging.info("Exiting...")
    sys.exit()


def confirm_config_path():
    if os.path.exists(CONFIG_PATH):
        return
    confirm_path(CONFIG_PATH)
    logging.info("Creating {}".format(CONFIG_PATH))
    os.mkdir(CONFIG_PATH)


def confirm_config_file():
    if os.path.exists(CONFIG_FILE):
        return
    confirm_path(CONFIG_FILE)
    logging.info("Configuring {}".format(CONFIG_FILE))
    config_dict = {}
    for key, val in Config().to_dict().items():
        if key in ["gcal_calendars", "notion_columns"]:
            continue
        if key == "gcal_default_calendar_name":
            gcal_mail = click.prompt("google_mail (e.g name@gmail.com)")
            config_dict["gcal_default_calendar_name"] = "Default"
            config_dict["gcal_calendars"] = {"Default": gcal_mail}
            continue
        config_dict[key] = click.prompt("{}".format(key), default=val)

    logging.info("Writing configured values to {}".format(CONFIG_FILE))
    Config(**config_dict).to_yaml()
    logging.info("Open {} to configure additional values.".format(CONFIG_FILE))


def confirm_credentials_file():
    if not os.path.exists(CREDENTIALS_FILE) and not os.path.exists(TOKEN_FILE):
        logging.error("{} nor {} exist".format(CREDENTIALS_FILE, TOKEN_FILE))
        logging.info(
            "Please follow the instructions on setting up the client_credentials.json: "
            "https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-credentials-for-google-calendar"
        )
        logging.info("Exiting...")
        sys.exit()
    if not os.path.exists(TOKEN_FILE):
        logging.info("{} does not exist".format(TOKEN_FILE))
        logging.info("Generating token file {}".format(TOKEN_FILE))
        GCalClient.get_credentials()


def configure():
    confirm_config_path()
    confirm_config_file()
    confirm_credentials_file()

    with open(CONFIG_FILE, "r") as yaml_file:
        yaml_cfg = yaml.safe_load(yaml_file)

    return Config(**yaml_cfg)
