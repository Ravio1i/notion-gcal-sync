import logging
import os

import yaml

from notion_gcal_sync.utils import Time

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".notion-gcal-sync")
CONFIG_FILE = os.path.join(CONFIG_PATH, "config.yml")


class Config:
    default_notion_columns = {
        "name": "Name",
        "date": "Date",
        "tags": "Tags",
        "description": "Description",
        "location": "Location",
        "last_updated_time": "Last Updated",
        "last_synced_time": "Last Synced",
        "gcal_event_id": "GCal event Id",
        "recurrent_event": "GCal Recurrence",
        "gcal_event_url": "GCal event url",
        "gcal_calendar_name": "Calendar",
        "gcal_calendar_id": "GCal calendar Id",
        "to_delete": "To Delete",
        "deleted": "Deleted",
        "read_only": "Read Only",
    }

    def __init__(
        self,
        default_event_length: int = 60,
        no_date_action: str = "skip",
        gcal_calendars=None,
        gcal_default_calendar_name: str = "Default",
        notion_database_url: str = None,
        notion_token: str = None,
        notion_columns: dict = None,
        timezone_name: str = "Europe/Berlin",
        timezone_diff: str = "+02:00",
    ):
        self.default_event_length = default_event_length
        self.no_date_action = no_date_action
        self.timezone_name = timezone_name
        self.timezone_diff = timezone_diff
        self.time = Time(timezone_name, timezone_diff)
        # GCAL
        self.gcal_calendars = gcal_calendars if gcal_calendars else {}
        self.gcal_default_calendar_name = gcal_default_calendar_name
        self.gcal_default_calendar_id = self.get_calendar_id(self.gcal_default_calendar_name)
        # NOTION
        self.notion_database_url = notion_database_url
        self.notion_token = notion_token

        self.notion_columns = notion_columns if notion_columns else self.default_notion_columns
        if not len([key for key in self.default_notion_columns.keys() if key in self.notion_columns.keys()]) == len(
            self.default_notion_columns.keys()
        ):
            raise ValueError

    @property
    def notion_database_url(self):
        return self._notion_database_url

    @notion_database_url.setter
    def notion_database_url(self, value):
        if not value or not value.startswith("https://www.notion.so/") or "?v=" not in value or value.endswith("?v="):
            logging.error(
                "Invalid database url: "
                "Should start with 'https://www.notion.so/'. "
                "Should contain '?v='. "
                "Should not end with '?v='. "
            )
            self._notion_database_url = None
            self.notion_database_id = None
            return

        if not value.endswith("&p="):
            value += "&p="
        self._notion_database_url = value
        self.notion_database_id = value[: value.index("?v=")].split("/")[-1]

    @property
    def default_event_length(self):
        return self._default_event_length

    @default_event_length.setter
    def default_event_length(self, value):
        if type(value) != int:
            logging.error("Invalid value {} for default_event_length. Defaulting to 60 minutes...".format(value))
            value = 60
        self._default_event_length = value

    @property
    def no_date_action(self):
        return self._no_date_action

    @no_date_action.setter
    def no_date_action(self, value):
        if value not in ["skip", "today"]:
            logging.error("Invalid no_date_action {}. Defaulting to skip".format(value))
            value = "skip"
        self._no_date_action = value

    @property
    def gcal_default_calendar_id(self):
        return self._gcal_default_calendar_id

    @gcal_default_calendar_id.setter
    def gcal_default_calendar_id(self, value):
        self._gcal_default_calendar_id = value

    def get_calendar_id(self, calendar_name: str) -> str:
        return self.gcal_calendars.get(calendar_name)

    def get_calendar_name(self, calendar_id: str) -> str or None:
        try:
            return list(self.gcal_calendars.keys())[list(self.gcal_calendars.values()).index(calendar_id)]
        except ValueError:
            return None

    def is_valid_calendar_name(self, calendar_name: str) -> bool:
        calendar_name = self.gcal_calendars.get(calendar_name)
        return True if calendar_name else False

    def is_valid_calendar_id(self, calendar_id: str) -> bool:
        calendar_id = self.get_calendar_name(calendar_id)
        return True if calendar_id else False

    def to_dict(self):
        config_dict = dict(
            (key.replace("_", "", 1), value) if key.startswith("_") else (key, value)
            for (key, value) in self.__dict__.items()
            if not key.startswith("__") and key != "cfg"
        )
        del config_dict["time"]
        del config_dict["notion_database_id"]
        del config_dict["gcal_default_calendar_id"]
        return config_dict

    def to_yaml(self):
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(self.to_dict(), file)
