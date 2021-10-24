import logging
from datetime import datetime

from notion_gcal_sync.config import Config
from notion_gcal_sync.events.Event import Event
from notion_gcal_sync.utils import Time


class NotionEvent(Event):
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
        notion_id: str = None,
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
        self.notion_id = notion_id
        # self.tags = tags

    @classmethod
    def from_api(cls, obj: dict, cfg: Config):
        props = obj["properties"]
        notion_id = obj["id"]
        notion_page_url = obj["url"]
        name = cls.get_name(props, cfg.notion_columns["name"])
        location = cls.get_text(props, cfg.notion_columns["location"])
        time_start, time_end = cls.get_time(props, cfg.notion_columns["date"])
        recurrent_event = cls.get_text(props, cfg.notion_columns["recurrent_event"])
        time_last_updated = cls.get_last_edited_time(props, cfg.notion_columns["last_updated_time"], cfg.time)
        time_last_synced = cls.get_text(props, cfg.notion_columns["last_synced_time"])
        description = cls.get_text(props, cfg.notion_columns["description"])
        gcal_event_id = cls.get_text(props, cfg.notion_columns["gcal_event_id"])
        gcal_page_url = cls.get_url(props, cfg.notion_columns["gcal_event_url"])
        gcal_calendar_name = cls.get_select(props, cfg.notion_columns["gcal_calendar_name"])
        gcal_calendar_id = cls.get_select(props, cfg.notion_columns["gcal_calendar_id"])
        read_only = cls.get_checkbox(props, cfg.notion_columns["read_only"])
        # tags = cls.get_multiselect(props, cfg.col_tags)
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
            notion_id,
            read_only,
            cfg,
        )

    @classmethod
    def get_name(cls, properties: dict, column: str) -> str:
        try:
            return properties.get(column, {})["title"][0]["text"]["content"]
        except (KeyError, IndexError):
            logging.error("Could not specify name for notion event")
            return ""

    @classmethod
    def get_last_edited_time(cls, properties: dict, column, time: Time) -> datetime:
        last_edited = properties.get(column, {})["last_edited_time"]
        last_edited_date = time.to_datetime(last_edited)
        return last_edited_date

    @classmethod
    def get_time(cls, properties: dict, column: str) -> (str, str):
        date = properties.get(column, {}).get("date")
        if not date:
            return None, None
        time_start = date.get("start")
        time_end = date.get("end") if date.get("end") else time_start
        return time_start, time_end

    @classmethod
    def get_text(cls, properties: dict, column: str) -> str:
        try:
            return properties.get(column, {})["rich_text"][0]["text"]["content"]
        except (KeyError, IndexError):
            return ""

    @classmethod
    def get_url(cls, properties: dict, column: str) -> str:
        return properties.get(column, {}).get("url", "")

    @classmethod
    def get_select(cls, properties: dict, column: str) -> str:
        select = properties.get(column, {}).get("select", {})
        if not select:
            return ""
        return select.get("name", "")

    @classmethod
    def get_multiselect(cls, properties: dict, column: str) -> list:
        try:
            multiselects = properties.get(column, {})["multi_select"]
            multiselect_names = [multiselect["name"] for multiselect in multiselects]
            return multiselect_names
        except KeyError:
            return []

    @classmethod
    def get_checkbox(cls, properties: dict, column: str) -> bool:
        try:
            return properties.get(column, {})["checkbox"]
        except KeyError:
            return False

    def body(self) -> dict:
        if self.cfg.time.is_date(self.time_start) and self.cfg.time.is_date(self.time_end):
            time_start = self.cfg.time.datetime_to_str_date(self.time_start)
            time_end = self.cfg.time.datetime_to_str_date(self.time_end)
        else:
            time_start = self.cfg.time.datetime_to_str(self.time_start)
            time_end = self.cfg.time.datetime_to_str(self.time_end)

        if self.time_start == self.time_end:
            time_end = None

        body = {
            "properties": {
                self.cfg.notion_columns["name"]: {"title": [{"text": {"content": self.name}}]},
                self.cfg.notion_columns["date"]: {"date": {"start": time_start, "end": time_end}},
                self.cfg.notion_columns["recurrent_event"]: {"rich_text": [{"text": {"content": self.recurrent_event}}]},
                self.cfg.notion_columns["description"]: {"rich_text": [{"text": {"content": self.description}}]},
                self.cfg.notion_columns["gcal_calendar_id"]: {"select": {"name": self.gcal_calendar_id}},
                self.cfg.notion_columns["gcal_calendar_name"]: {"select": {"name": self.gcal_calendar_name}},
                self.cfg.notion_columns["location"]: {"rich_text": [{"text": {"content": self.location}}]},
                self.cfg.notion_columns["gcal_event_id"]: {"rich_text": [{"text": {"content": self.gcal_event_id}}]},
                self.cfg.notion_columns["last_synced_time"]: {"rich_text": [{"text": {"content": self.cfg.time.now()}}]},
                self.cfg.notion_columns["gcal_event_url"]: {"url": self.gcal_page_url},
                self.cfg.notion_columns["read_only"]: {"checkbox": bool(self.read_only)},
            },
        }
        logging.info(body)
        return body
