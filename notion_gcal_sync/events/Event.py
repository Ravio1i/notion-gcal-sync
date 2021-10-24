import logging
from datetime import datetime, timedelta

from notion_gcal_sync.config import Config


class Event:
    def __init__(
        self,
        name: str = None,
        description: str = None,
        location: str = None,
        gcal_event_id: str = None,
        gcal_calendar_name: str = None,
        gcal_calendar_id: str = None,
        time_start: str or datetime = None,
        time_end: str or datetime = None,
        recurrent_event: str = None,
        time_last_updated: datetime = None,
        time_last_synced: str = None,
        notion_page_url: str = None,
        gcal_page_url: str = None,
        read_only: bool = None,
        cfg: Config = None,
    ):
        self.cfg = cfg if cfg else Config()
        # Properties
        self.name = name
        self.description = description
        self.location = location
        self.gcal_event_id = gcal_event_id

        self.gcal_calendar_id, self.gcal_calendar_name = self.set_calendar(gcal_calendar_id, gcal_calendar_name)
        # Check if valid calendar name differs from the valid calendar name behind the id
        if self.gcal_calendar_name != self.cfg.get_calendar_name(self.gcal_calendar_id):
            self.gcal_calendar_id = self.cfg.get_calendar_id(self.gcal_calendar_name)

        self.time_start = self.cfg.time.to_datetime(time_start)
        self.time_end = self.cfg.time.to_datetime(time_end)
        # Apply default length when no end is specified but a time is given
        if (
            self.time_start
            and self.time_end
            and not self.cfg.time.is_date(self.time_start)
            and not self.cfg.time.is_date(self.time_end)
            and self.time_start == self.time_end
        ):
            self.time_end = self.time_start + timedelta(minutes=self.cfg.default_event_length)

        self.recurrent_event = recurrent_event
        self.time_last_updated = time_last_updated
        self.time_last_synced = time_last_synced
        self.notion_page_url = notion_page_url
        self.gcal_page_url = gcal_page_url
        self.read_only = read_only

    def to_dict(self):
        return dict(
            (key.replace("_", "", 1), value) if key.startswith("_") else (key, value)
            for (key, value) in self.__dict__.items()
            if not key.startswith("__") and key != "cfg"
        )

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value:
            self._description = ""
            return
        if len(value) > 2000:
            logging.warning(
                "Description of Event '{}' with {} characters too long for Notion (> 2000)".format(self.name, len(value))
            )
            self._description = value[:2000]
            return
        self._description = value

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        self._read_only = True if value in [True, "True"] else False

    def set_calendar(self, gcal_calendar_id: str, gcal_calendar_name: str) -> (str, str):
        """
        Set calendar id and calendar name depending on the values
        :param gcal_calendar_id:
        :param gcal_calendar_name:
        :return: gcal_calendar_id, gcal_calendar_name
        """
        # Valid calendar name and valid calendar id
        if not gcal_calendar_id and not gcal_calendar_name:
            return self.cfg.gcal_default_calendar_id, self.cfg.gcal_default_calendar_name
        if self.cfg.is_valid_calendar_name(gcal_calendar_name) and self.cfg.is_valid_calendar_id(gcal_calendar_id):
            return gcal_calendar_id, gcal_calendar_name
        # Invalid calendar name but valid calendar id -> derive calendar name from id
        if not self.cfg.is_valid_calendar_name(gcal_calendar_name) and self.cfg.is_valid_calendar_id(gcal_calendar_id):
            return gcal_calendar_id, self.cfg.get_calendar_name(gcal_calendar_id)
        # Invalid calendar id but valid calendar name -> derive calendar id from name
        if not self.cfg.is_valid_calendar_id(gcal_calendar_id) and self.cfg.is_valid_calendar_name(gcal_calendar_name):
            return self.cfg.get_calendar_id(gcal_calendar_name), gcal_calendar_name
        # Internal calendar from Google not to tweak with
        if gcal_calendar_name == "Google Calendar":
            return "skip", "skip"

        logging.debug(
            'Different organizer calendar "{}" for event "{}". Using default calendar {}'.format(
                gcal_calendar_id, self.name, self.cfg.get_calendar_id(self.cfg.gcal_default_calendar_name),
            )
        )
        return self.cfg.gcal_default_calendar_id, self.cfg.gcal_default_calendar_name
