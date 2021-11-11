import logging
import re
from datetime import datetime, date

import pendulum


class Time:
    def __init__(self, timezone_name: str):
        self.timezone_name = timezone_name
        self.timezone = pendulum.timezone(self.timezone_name)

    @staticmethod
    def now() -> str:
        return datetime.now().isoformat("T", "minutes")

    @staticmethod
    def format_str(dt: str) -> str or None:
        """Change Z indicator for UTC with +00:00"""
        if not dt:
            logging.error("Date {} is not str format".format(dt))
            return None
        return dt.replace("Z", "+00:00")

    @staticmethod
    def format_datetime(dt: datetime) -> datetime or None:
        """We do not need seconds and microseconds"""
        if not dt:
            logging.error("Date {} is not datetime format".format(dt))
            return None
        return dt.replace(second=0, microsecond=0)

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

    def to_str(self, dt: str or datetime or date):
        if type(dt) == str:
            return self.format_str(dt)
        if type(dt) == date:
            return dt.strftime("%Y-%m-%d")
        if type(dt) == datetime:
            return dt.isoformat("T", "seconds")
        logging.error("Date {} is in some other format".format(dt))
        return None

    def to_datetime(self, dt: str or datetime or date) -> datetime or date or None:
        if type(dt) == date:
            return dt
        if type(dt) == datetime:
            return self.format_datetime(dt)
        if type(dt) == str:
            dt = self.format_str(dt)
            if self.is_date(dt):
                return datetime.strptime(dt, "%Y-%m-%d").date()
            dt = self.format_datetime(datetime.fromisoformat(dt))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=self.timezone)
            dt = dt.astimezone(self.timezone)
            return dt
        logging.error("Date {} is in some other format".format(dt))
        return None

    def format(self, dt: str or datetime or date) -> str or None:
        dt = self.to_datetime(dt)
        dt = self.to_str(dt)
        return dt
