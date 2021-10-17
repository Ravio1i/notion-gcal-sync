import logging

from .utils import Time


class Config:
    def __init__(self, default_event_length: int, no_date_action: str, default_calendar_id: str, default_calendar_name: str,
                 calendars: dict, database_url: str, token: str,  columns: dict,  time: Time):
        # GENERAL
        self.default_event_length = default_event_length
        self.no_date_action = no_date_action

        # GCAL
        self.default_calendar_id = default_calendar_id
        self.default_calendar_name = default_calendar_name
        self.calendars = calendars

        # NOTION
        self.database_url = database_url
        self.token = token
        self.col_name = columns['name']
        self.col_date = columns['date']
        self.col_recurrent_event = columns['recurrent_event']
        self.col_tags = columns['tags']
        self.col_description = columns['description']
        self.col_location = columns['location']
        self.col_last_updated_time = columns['last_updated_time']
        self.col_last_synced_time = columns['last_synced_time']
        self.col_gcal_event_id = columns['gcal_event_id']
        self.col_gcal_event_url = columns['gcal_event_url']
        self.col_gcal_calendar_name = columns['gcal_calendar_name']
        self.col_gcal_calendar_id = columns['gcal_calendar_id']
        self.col_to_delete = columns['to_delete']
        self.col_deleted = columns['deleted']
        self.col_read_only = columns['read_only']

        # TIME
        self.time = time

    @property
    def database_url(self):
        return self._database_url

    @database_url.setter
    def database_url(self, value):
        self._database_url = value
        if "?v=" in value and value.startswith("https://www.notion.so/") and value.endswith("&p="):
            self.database_id = self.database_url[:self.database_url.index('?v=')].split('/')[-1]
            return
        logging.error("Invalid database url. Cannot get database id")
        self.database_id = None

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
        if value not in ['skip', 'today']:
            logging.error("Invalid no_date_action {}. Defaulting to skip".format(value))
            value = 'skip'
        self._no_date_action = value

    def get_calendar_id(self, calendar_name: str) -> str:
        return self.calendars.get(calendar_name)

    def get_calendar_name(self, calendar_id: str) -> str or None:
        try:
            return list(self.calendars.keys())[list(self.calendars.values()).index(calendar_id)]
        except ValueError:
            return None

    def is_valid_calendar_name(self, calendar_name: str) -> bool:
        calendar_name = self.calendars.get(calendar_name)
        return True if calendar_name else False

    def is_valid_calendar_id(self, calendar_id: str) -> bool:
        calendar_id = self.get_calendar_name(calendar_id)
        return True if calendar_id else False
