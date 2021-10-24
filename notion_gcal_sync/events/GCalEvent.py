import logging
from datetime import datetime, timedelta

from notion_gcal_sync.config import Config
from notion_gcal_sync.events.Event import Event
from notion_gcal_sync.utils import Time


class GCalEvent(Event):
    def __init__(
        self,
        name: str = None,
        description: str = None,
        location: str = None,
        gcal_event_id: str = None,
        gcal_calendar_name: str = None,
        gcal_calendar_id: str = None,
        time_start: datetime = None,
        time_end: datetime = None,
        recurrent_event: str = None,
        time_last_updated: datetime = None,
        time_last_synced: str = None,
        notion_page_url: str = None,
        gcal_page_url: str = None,
        color_id: str = None,
        read_only: bool = None,
        cfg: Config = None,
    ):
        super().__init__(
            name,
            description,
            location,
            gcal_event_id,
            gcal_calendar_name,
            gcal_calendar_id,
            time_start,
            time_end,
            recurrent_event,
            time_last_updated,
            time_last_synced,
            notion_page_url,
            gcal_page_url,
            read_only,
            cfg,
        )
        self.color_id = color_id

    @classmethod
    def from_api(cls, obj, cfg: Config, time: Time):
        gcal_event_id = obj.get("id", "")
        name = obj.get("summary", "")
        gcal_calendar_id, gcal_calendar_name = cls.get_calendar(obj)
        location = obj.get("location", "")
        time_start, time_end, time_last_updated = cls.get_time(obj, time)
        recurrent_event = cls.get_recurrent_event(obj)
        notion_page_url, time_last_synced, description = cls.get_meta(obj)
        gcal_page_url = obj.get("htmlLink", "")
        color_id = obj.get("colorId", "")
        read_only = obj.get("privateCopy", False)
        return cls(
            name,
            description,
            location,
            gcal_event_id,
            gcal_calendar_name,
            gcal_calendar_id,
            time_start,
            time_end,
            recurrent_event,
            time_last_updated,
            time_last_synced,
            notion_page_url,
            gcal_page_url,
            color_id,
            read_only,
            cfg,
        )

    @classmethod
    def get_meta(cls, obj: dict) -> (str, str):
        """Get source url == page_url, source_title == Sync Status and description that may get updated from source url"""
        source = obj.get("source")
        description = obj.get("description", "")
        if not source:
            return "", "", description
        source_url = source.get("url")
        source_title = source.get("title")
        if not source_title.startswith("Notion at"):
            description = "Source: {}\n{}".format(source_url, description)
            source_url = source_title = ""
        return source_url, source_title.replace("Notion at ", ""), description

    @classmethod
    def get_time(cls, obj: dict, time: Time) -> (datetime, datetime):
        time_last_updated = time.to_datetime(obj.get("updated"))
        try:
            time_start = obj.get("start", {})["dateTime"]
            time_end = obj.get("end", {})["dateTime"]
            return time_start, time_end, time_last_updated
        except KeyError:
            time_start = time.to_datetime(obj.get("start", {})["date"])
            time_end = time.to_datetime(obj.get("end", {})["date"]) - timedelta(days=1)
        return time_start, time_end, time_last_updated

    @classmethod
    def get_calendar(cls, obj: dict) -> (str, str):
        """Get calendar id from organizer. This may differ when the event is created from some one else"""
        organizer = obj.get("organizer", {})
        gcal_calendar_id = organizer.get("email")
        gcal_calendar_name = organizer.get("displayName")
        return gcal_calendar_id, gcal_calendar_name

    @classmethod
    def get_recurrent_event(cls, obj: dict) -> str:
        """Get event id of original event if this event is occurrence of recurrence"""
        return obj.get("recurringEventId", "")

    @property
    def body(self):
        body = {
            "summary": self.name,
            "description": self.description,
            "location": self.location,
            "source": {"title": "Notion at " + self.time_last_synced, "url": self.notion_page_url},
        }

        time_end = self.time_end
        # utils is just a date
        if Time.is_date(self.time_start) and Time.is_date(self.time_end):
            logging.debug('Updating end of date of "{}" by one day to get all day event'.format(self.name))
            time_end = self.time_end + timedelta(days=1)

        if self.cfg.time.is_date(self.time_start) and self.cfg.time.is_date(self.time_end):
            body["start"] = {
                "date": self.cfg.time.datetime_to_str_date(self.time_start),
                "timeZone": self.cfg.time.timezone_name,
            }
            body["end"] = {
                "date": self.cfg.time.datetime_to_str_date(time_end),
                "timeZone": self.cfg.time.timezone_name,
            }
        else:
            body["start"] = {
                "dateTime": self.cfg.time.datetime_to_str(self.time_start),
                "timeZone": self.cfg.time.timezone_name,
            }
            body["end"] = {
                "dateTime": self.cfg.time.datetime_to_str(time_end),
                "timeZone": self.cfg.time.timezone_name,
            }

        logging.info(body)
        return body
