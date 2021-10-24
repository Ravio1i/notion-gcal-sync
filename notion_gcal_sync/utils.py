import logging
import re
from datetime import datetime, timedelta, timezone


class Time:
    def __init__(self, timezone_name: str, timezone_diff: str):
        self.timezone_name = timezone_name
        self.timezone_diff = timezone_diff
        hours, minutes = timezone_diff.split(":")
        self.timezone_diff_delta = timedelta(hours=int(hours), minutes=int(minutes))

    @staticmethod
    def is_date(dt: datetime or str) -> bool or None:
        """Return if date range is just a date without time"""
        if type(dt) == str:
            date_match = re.match(r"[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$", dt)
            return True if date_match else False
        if type(dt) == datetime:
            return dt.hour == 0 and dt.minute == 0 if not dt.tzinfo else False
        logging.error("Date {} is in some other format".format(dt))
        return None

    @staticmethod
    def datetime_to_str(dt: datetime) -> str or None:
        if type(dt) != datetime:
            return None
        return dt.isoformat("T", "seconds")

    @staticmethod
    def datetime_to_str_date(dt: datetime) -> str or None:
        if not dt:
            return None
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def now() -> str:
        return datetime.now().isoformat("T", "minutes")

    def to_datetime(self, dt: str or datetime) -> datetime or None:
        if type(dt) == datetime:
            return dt
        if type(dt) == str:
            return self.str_to_datetime(dt)
        logging.error("Date {} is in some other format".format(dt))
        return None

    def str_to_datetime(self, date_str: str) -> datetime or None:
        if not date_str:
            return None

        # Replace UTC with +00:00
        date_str = date_str.replace("Z", "+00:00")

        if self.is_date(date_str):
            return datetime.fromisoformat(date_str)

        dt = datetime.fromisoformat(date_str).replace(second=0, microsecond=0)
        offset = datetime.utcoffset(dt)
        if offset is not None:
            dt = dt + (self.timezone_diff_delta - offset)
        return dt.replace(tzinfo=timezone(self.timezone_diff_delta))
