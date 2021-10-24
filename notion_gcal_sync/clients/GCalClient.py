import logging
import os
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from notion_gcal_sync.config import Config
from notion_gcal_sync.events.GCalEvent import GCalEvent

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".notion-gcal-sync")


class GCalClient:
    """The client class used to perform requests against google api"""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.credentials = self.get_credentials()
        self.service = build("calendar", "v3", credentials=self.credentials, cache_discovery=False)
        self.calendar = self.service.calendars().get(calendarId=self.cfg.gcal_default_calendar_id).execute()

    @staticmethod
    def get_credentials():
        scopes = ["https://www.googleapis.com/auth/calendar"]
        credentials = None
        token_path = os.path.join(CONFIG_PATH, "token.json")
        if os.path.exists(os.path.join(CONFIG_PATH, token_path)):
            credentials = Credentials.from_authorized_user_file(token_path, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials_path = os.path.join(CONFIG_PATH, "client_credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(credentials.to_json())
        return credentials

    def get_event(self, gcal_calendar_id: str, gcal_event_id: str):
        """
        Get google calendar event from GCalEvent
        :return: dict: response object from google calendar update
        """
        return self.service.events().get(calendarId=gcal_calendar_id, eventId=gcal_event_id).execute()

    def list_events(self, calendar_id: str) -> List[dict]:
        """
        Get all events from the calendar id, transform them into GCalEvent to have a formal structure.
        Skips removed (cancelled) events and eventFs with no name (summary=None)
        :param calendar_id: Google calendar id (**@group.calendar.google.com)
        :return: List[dict]: List of all events as dictionary in format of GCalEvent
        """
        page_token = None
        max_results = 2500
        gcal_event_items = []
        gcal_event_count = 0

        logging.info("Fetching events from calendar: {}".format(self.cfg.get_calendar_name(calendar_id)))
        while True:
            gcal_events_res = (
                self.service.events()
                .list(
                    calendarId=calendar_id, pageToken=page_token, timeZone=self.cfg.time.timezone_name, maxResults=max_results,
                )
                .execute()
            )
            gcal_event_count += len(gcal_events_res["items"])
            print("Found {} events".format(gcal_event_count), end="\r")

            for event in gcal_events_res["items"]:

                if event["status"] == "cancelled":
                    logging.debug('Event "{}" is  cancelled. Skipping...'.format(event.get("id", "")))
                    continue

                if not event.get("summary"):
                    logging.error('Event "{}" at "{}" has no name. Skipping...'.format(event.get("id", ""), event["start"]))
                    continue

                if event.get("recurrence"):
                    logging.debug("Event {} is recurrent source .Skipping...".format(event["summary"]))
                    continue

                gcal_event = GCalEvent.from_api(event, self.cfg, self.cfg.time)
                if gcal_event.gcal_calendar_id == "skip":
                    logging.debug("Event {} id is not valid. Skipping...".format(event["summary"]))
                    continue

                if gcal_event.recurrent_event:
                    logging.debug('Using gcal event link for "{}" as recurrence reference'.format(gcal_event.name))
                    gcal_res = self.get_event(gcal_event.gcal_calendar_id, gcal_event.gcal_event_id)
                    gcal_event.recurrent_event = gcal_res["htmlLink"]

                gcal_event_items.append(gcal_event.to_dict())

            page_token = gcal_events_res.get("nextPageToken")
            if not page_token:
                break

        logging.info("Found {} events from calendar: {}".format(gcal_event_count, self.cfg.get_calendar_name(calendar_id)))
        return gcal_event_items

    def create_event(self, gcal_event: GCalEvent):
        """
        Create an event in google calendar
        :param gcal_event: GCalEvent
        :return: dict: response object from google calendar update
        """
        res = self.service.events().insert(calendarId=gcal_event.gcal_calendar_id, body=gcal_event.body).execute()
        return res

    def update_event(self, gcal_event: GCalEvent) -> dict or None:
        """
        Updates an event in google calendar
        :param gcal_event: GCalEvent
        :return: dict: response from google calendar update
        """
        # try:
        if gcal_event.read_only:
            logging.info('Not updating in gcal read only event "{}"'.format(gcal_event.name))
            return
        return (
            self.service.events()
            .update(calendarId=gcal_event.gcal_calendar_id, eventId=gcal_event.gcal_event_id, body=gcal_event.body,)
            .execute()
        )
        # TODO: what to do about forbidden
        # except:
        #    return None

    def delete_event(self, gcal_event: GCalEvent) -> dict or None:
        """
        Deleting an event from google calendar
        :param gcal_event: GCalEvent
        :return: dict: response
        """
        if gcal_event.read_only:
            logging.info('Not deleting in gcal read only event "{}"'.format(gcal_event.name))
            return
        return self.service.events().delete(calendarId=gcal_event.gcal_calendar_id, eventId=gcal_event.gcal_event_id).execute()

    def update_notion_link(self, gcal_event: GCalEvent, notion_page_url: str):
        if notion_page_url == gcal_event.notion_page_url:
            return
        logging.info('- Updating notion page url for event "{}" in GCal'.format(gcal_event.name))
        gcal_event.notion_page_url = notion_page_url
        self.update_event(gcal_event)
