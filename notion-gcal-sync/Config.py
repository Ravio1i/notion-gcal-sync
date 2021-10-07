import logging
from utils.Time import Time


class Config:
    def __init__(self, default_calendar_id: str, default_calendar_name: str, calendars: dict, default_event_length: int,
                 database_url: str, token: str, no_date_action: str, columns: dict,  time: Time):
        self.time = time
        # GCAL
        self.default_calendar_id = default_calendar_id
        self.default_calendar_name = default_calendar_name
        self.calendars = calendars
        self.default_event_length = default_event_length
        # NOTION
        self.database_url = database_url
        self.database_id = database_url[:database_url.index('?v=')].split('/')[-1]
        self.token = token
        if no_date_action not in ['skip', 'today']:
            logging.error("Invalid no_date_action {}. Defaulting to skip".format(no_date_action))
            no_date_action = 'skip'
        self.no_date_action = no_date_action
        # Database Columns
        self.col_name = columns['name']
        self.col_date = columns['date']
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
