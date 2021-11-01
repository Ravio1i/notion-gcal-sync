import logging
import re
from datetime import datetime, date

import pytz


class Time:
    def __init__(self, timezone_name: str):
        self.timezone_name = timezone_name
        self.timezone = pytz.timezone(self.timezone_name)

    @staticmethod
    def is_date(dt: datetime or str) -> bool or None:
        """Return if date range is just a date without time"""
        if type(dt) == str:
            date_match = re.match(r"[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$", dt)
            return True if date_match else False
        if type(dt) == date:
            return True
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
        return datetime.now().isoformat("T", "seconds")

    def to_datetime(self, dt: str or datetime or date) -> datetime or date or None:
        if type(dt) == datetime or type(dt) == date:
            return dt
        if type(dt) == str:
            return self.str_to_datetime(dt)
        logging.error("Date {} is in some other format".format(dt))
        return None

    def str_to_datetime(self, date_str: str) -> datetime or date or None:
        if not date_str:
            return None

        # Replace UTC with +00:00
        date_str = date_str.replace("Z", "+00:00")

        if self.is_date(date_str):
            return datetime.strptime(date_str, "%Y-%m-%d").date()

        dt = datetime.fromisoformat(date_str).replace(second=0, microsecond=0)
        return dt.astimezone(self.timezone)
