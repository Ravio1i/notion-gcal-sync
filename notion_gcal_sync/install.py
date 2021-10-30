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
CLIENT_SECRET_FILE = os.path.join(CONFIG_PATH, "client_secret.json")


def confirm_create_path(path: str) -> bool:
    logging.info("{} does not exist".format(path))
    if click.confirm("Create non-existing {}?".format(path), default=True):
        return True
    return False


def config_path_created() -> bool:
    if os.path.exists(CONFIG_PATH):
        return True
    if not confirm_create_path(CONFIG_PATH):
        return False
    logging.info("Creating {}".format(CONFIG_PATH))
    os.mkdir(CONFIG_PATH)
    return True


def config_file_created() -> bool:
    if os.path.exists(CONFIG_FILE):
        return True
    if not confirm_create_path(CONFIG_FILE):
        return False
    logging.info("Configuring {}".format(CONFIG_FILE))
    config_dict = {}
    for key, val in Config().to_dict().items():
        if key in ["gcal_calendars", "notion_columns"]:
            continue
        if key == "gcal_default_calendar_name":
            gcal_mail = click.prompt(text="google_mail (e.g name@gmail.com)", default=None)
            config_dict["gcal_default_calendar_name"] = "Default"
            config_dict["gcal_calendars"] = {"Default": gcal_mail}
            continue
        config_dict[key] = click.prompt(text="{}".format(key), default=val)

    logging.info("Writing configured values to {}".format(CONFIG_FILE))
    Config(**config_dict).to_yaml()
    logging.info("Open {} to configure additional values.".format(CONFIG_FILE))
    return True


def client_secret_created() -> bool:
    if not os.path.exists(TOKEN_FILE) and os.path.exists(CLIENT_SECRET_FILE):
        logging.info("{} does not exist".format(TOKEN_FILE))
        logging.info("Generating token file {}".format(TOKEN_FILE))
        GCalClient.get_credentials()
    if os.path.exists(TOKEN_FILE):
        return True
    logging.error("{} nor {} exist".format(CLIENT_SECRET_FILE, TOKEN_FILE))
    logging.info(
        "Please follow the instructions on setting up the client_secret.json: "
        "https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-credentials-for-google-calendar"
    )
    return False


def configure():
    confirmed = config_path_created() and config_file_created() and client_secret_created()
    if not confirmed:
        logging.info("Exiting...")
        sys.exit()

    with open(CONFIG_FILE, "r") as yaml_file:
        yaml_cfg = yaml.safe_load(yaml_file)

    return Config(**yaml_cfg)
