from datetime import datetime, timedelta

from Config import Config

import logging


class Event:
    def __init__(self, name: str = None, description: str = None, location: str = None, gcal_event_id: str = None,
                 gcal_calendar_name: str = None, gcal_calendar_id: str = None, time_start: datetime = None, time_end: datetime = None,
                 time_last_updated: datetime = None, time_last_synced: str = None, notion_page_url: str = None,
                 gcal_page_url: str = None, cfg: Config = None):
        self.cfg = cfg
        # Properties
        self.name = name
        self.description = description
        self.location = location
        self.gcal_event_id = gcal_event_id

        if self.cfg.is_valid_calendar_name(gcal_calendar_name) and self.cfg.is_valid_calendar_id(gcal_calendar_id):
            self.gcal_calendar_name = gcal_calendar_name
            self.gcal_calendar_id = gcal_calendar_id
        elif not self.cfg.is_valid_calendar_name(gcal_calendar_name) and self.cfg.is_valid_calendar_id(gcal_calendar_id):
            self.gcal_calendar_name = self.cfg.get_calendar_name(gcal_calendar_id)
            self.gcal_calendar_id = gcal_calendar_id
        elif not self.cfg.is_valid_calendar_id(gcal_calendar_id) and self.cfg.is_valid_calendar_name(gcal_calendar_name):
            self.gcal_calendar_id = self.cfg.get_calendar_id(gcal_calendar_name)
            self.gcal_calendar_name = gcal_calendar_name
        else:
            logging.warning('Could not find id for "{}". Using default calendar {}'
                            .format(gcal_calendar_name, self.cfg.default_calendar_id))
            self.gcal_calendar_name = self.cfg.default_calendar_name
            self.gcal_calendar_id = self.cfg.default_calendar_id

        # Check if calendar differs
        if self.gcal_calendar_name != self.cfg.get_calendar_name(self.gcal_calendar_id):
            self.gcal_calendar_id = self.cfg.get_calendar_id(self.gcal_calendar_name)

        self.time_start = cfg.time.to_datetime(time_start)
        self.time_end = cfg.time.to_datetime(time_end)
        # Apply default length
        if not self.cfg.time.is_date(self.time_start) and not self.cfg.time.is_date(self.time_end) and self.time_start == self.time_end:
            self.time_end = self.time_start + timedelta(minutes=self.cfg.default_event_length)

        self.time_last_updated = time_last_updated
        self.time_last_synced = time_last_synced
        self.notion_page_url = notion_page_url
        self.gcal_page_url = gcal_page_url

    def dict_from_class(self):
        return dict(
            (key, value)
            for (key, value) in self.__dict__.items()
            if not key.startswith('_') and key != "cfg"
        )
