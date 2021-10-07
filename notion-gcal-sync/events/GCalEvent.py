import logging
from datetime import datetime, timedelta
from typing import Union, Optional, Any, TypedDict

from Config import Config
from events.Event import Event
from utils.Time import Time


class GCalEvent(Event):
    def __init__(self, name: str = None, description: str = None, location: str = None, gcal_event_id: str = None,
                 gcal_calendar_name: str = None, gcal_calendar_id: str = None, time_start: datetime = None, time_end: datetime = None,
                 time_last_updated: datetime = None, time_last_synced: str = None, notion_page_url: str = None, gcal_page_url: str = None,
                 color_id: str = None, cfg: Config = None):
        super().__init__(name, description, location, gcal_event_id, gcal_calendar_name, gcal_calendar_id, time_start, time_end,
                         time_last_updated, time_last_synced, notion_page_url, gcal_page_url, cfg)
        self.color_id = color_id

    @classmethod
    def from_api(cls, obj, cfg: Config, time: Time):
        gcal_event_id = obj.get('id', '')
        name = obj.get('summary', '')
        description = obj.get('description', '')
        gcal_calendar_id = obj.get('organizer', {}).get('email')
        gcal_calendar_name = obj.get('organizer', {}).get('displayName')
        location = obj.get('location', '')
        time_start, time_end, time_last_updated = cls.get_time(obj, time)
        notion_page_url, time_last_synced = cls.get_source(obj)
        gcal_page_url = obj.get('htmlLink', '')
        color_id = obj.get('colorId', '')
        return cls(name, description, location, gcal_event_id, gcal_calendar_name, gcal_calendar_id, time_start, time_end,
                   time_last_updated, time_last_synced, notion_page_url, gcal_page_url, color_id, cfg)

    @classmethod
    def get_source(cls, obj: dict) -> (str, str):
        source = obj.get('source')
        if not source:
            return '', ''
        return source.get('url'), source.get('title').replace('Notion at ', '')

    @classmethod
    def get_time(cls, obj: dict, time: Time) -> (datetime, datetime):
        time_last_updated = time.to_datetime(obj.get('updated'))
        try:
            time_start = obj.get('start', { })['dateTime']
            time_end = obj.get('end', {})['dateTime']
            return time_start, time_end, time_last_updated
        except KeyError:
            time_start = time.to_datetime(obj.get('start', {})['date'])
            time_end = time.to_datetime(obj.get('end', {})['date']) - timedelta(days=1)
        return time_start, time_end, time_last_updated

    def body(self):
        body: dict[str, Union[str, None, dict[str, Optional[str]], dict[str, Union[dict[str, Any], Any]], TypedDict]] = {
            'summary': self.name,
            'description': self.description,
            'location': self.location,
            'source': {
                'title': 'Notion at ' + self.time_last_synced,
                'url': self.notion_page_url,
            }
        }

        time_end = self.time_end
        # utils is just a date
        if Time.is_date(self.time_start) and Time.is_date(self.time_end):
            time_end = (self.time_end + timedelta(days=1))

        if self.cfg.time.is_date(self.time_start) and self.cfg.time.is_date(self.time_end):
            body['start'] = {
                'date': self.cfg.time.datetime_to_str_date(self.time_start),
                'timeZone': self.cfg.time.timezone_name,
            }
            body['end'] = {
                'date': self.cfg.time.datetime_to_str_date(time_end),
                'timeZone': self.cfg.time.timezone_name,
            }
        else:
            body['start'] = {
                'dateTime': self.cfg.time.datetime_to_str(self.time_start),
                'timeZone': self.cfg.time.timezone_name,
            }
            body['end'] = {
                'dateTime': self.cfg.time.datetime_to_str(time_end),
                'timeZone': self.cfg.time.timezone_name,
            }

        logging.info(body)
        return body
