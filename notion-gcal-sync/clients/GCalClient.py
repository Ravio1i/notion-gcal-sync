import logging
import os
from typing import List

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from Config import Config
from events.GCalEvent import GCalEvent

current_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(os.path.dirname(current_dir))


class GCalClient:
    """The client class used to perform requests against google api"""
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        credentials = None
        token_path = os.path.join(root_dir, 'token.json')
        if os.path.exists(os.path.join(root_dir, token_path)):
            credentials = Credentials.from_authorized_user_file(token_path, self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials_path = os.path.join(root_dir, 'client_credentials.json')
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.scopes)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(credentials.to_json())

        self.service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
        self.calendar = self.service.calendars().get(calendarId=self.cfg.default_calendar_id).execute()

    def get_event(self, gcal_event: GCalEvent):
        """
        Get google calendar event from GCalEvent
        :param gcal_event: GCalEvent
        :return: dict: response object from google calendar update
        """
        return self.service.events().get(calendarId=gcal_event.gcal_calendar_id, eventId=gcal_event.gcal_event_id).execute()

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
        logging.info('Fetching events from calendar: {}'.format(self.cfg.get_calendar_name(calendar_id)))
        while True:
            gcal_events_res = self.service.events().list(calendarId=calendar_id, pageToken=page_token, timeZone=self.cfg.time.timezone_name,
                                                         maxResults=max_results).execute()
            gcal_event_count += len(gcal_events_res['items'])
            print('Found {} events'.format(gcal_event_count), end='\r')
            for event in gcal_events_res['items']:
                if event['status'] == 'cancelled':
                    continue
                if not event.get('summary'):
                    logging.error('Event at {} does not have a name'.format(event['start']))
                    continue

                gcal_event = GCalEvent.from_api(event, self.cfg, self.cfg.time).dict_from_class()
                gcal_event_items.append(gcal_event)
            page_token = gcal_events_res.get('nextPageToken')
            if not page_token:
                break

        logging.info('Found {} events from calendar: {}'.format(gcal_event_count, self.cfg.get_calendar_name(calendar_id)))
        return gcal_event_items

    def create_event(self, gcal_event: GCalEvent):
        """
        Create an event in google calendar
        :param gcal_event: GCalEvent
        :return: dict: response object from google calendar update
        """
        res = self.service.events().insert(calendarId=gcal_event.gcal_calendar_id, body=gcal_event.body()).execute()
        return res

    def update_event(self, gcal_event: GCalEvent) -> dict or None:
        """
        Updates an event in google calendar
        :param gcal_event: GCalEvent
        :return: dict: response from google calendar update
        """
        # try:
        return self.service.events().update(calendarId=gcal_event.gcal_calendar_id, eventId=gcal_event.gcal_event_id,
                                            body=gcal_event.body()).execute()
        # TODO: what to do about forbidden
        # except:
        #    return None

    def delete_event(self, gcal_event: GCalEvent) -> dict:
        """
        Deleting an event from google calendar
        :param gcal_event: GCalEvent
        :return: dict: response
        """
        return self.service.events().delete(calendarId=gcal_event.gcal_calendar_id, eventId=gcal_event.gcal_event_id).execute()
