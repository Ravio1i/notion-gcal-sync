import logging

from datetime import date

from notion_client import Client

from Config import Config
from events.NotionEvent import NotionEvent


class NotionClient:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.client = Client(auth=self.cfg.token)

    def list_events(self, delete: bool = False):
        notion_events = []
        notion_events_res = self.query_items(delete)
        logging.info("Found {} event(s) in Notion".format(len(notion_events_res)))
        for i, obj in enumerate(notion_events_res):
            notion_event = NotionEvent.from_api(obj, self.cfg)

            if not notion_event.time_start and self.cfg.no_date_action == 'skip':
                logging.warning('Skipping event {} with no date specified'.format(notion_event.name))
                continue

            if not notion_event.time_start and self.cfg.no_date_action == 'today':
                logging.warning('Event {} with no date set to today'.format(notion_event.name))
                notion_event.time_start = notion_event.time_end = date.today()

            notion_events.append(notion_event.dict_from_class())
        return notion_events

    def query_items(self, delete: bool = False):
        return self.client.databases.query(
            **{
                'database_id': self.cfg.database_id,
                'filter': {
                    'and': [
                        {
                            'property': self.cfg.col_to_delete,
                            'checkbox': {
                                'equals': delete
                            }
                        }, {
                            'property': self.cfg.col_deleted,
                            'checkbox': {
                                'equals': False
                            }
                        }]
                }
            })['results']

    def create_event(self, notion_event: NotionEvent) -> dict:
        header = {"parent": {"database_id": self.cfg.database_id}}
        return self.client.pages.create(**header, **notion_event.body())

    def update_event(self, notion_event: NotionEvent) -> dict:
        """This checks off that the event has been put on Google Calendar"""
        return self.client.pages.update(notion_event.notion_id, **notion_event.body())

    def delete_event(self, notion_event: NotionEvent) -> dict:
        """Currently only puts match to True as notion api does not support delete"""
        return self.client.pages.update(notion_event.notion_id, **{
            "properties": {
                self.cfg.col_deleted: {
                    'checkbox': True
                }
            }
        })

    def set_sync_error(self, notion_event: NotionEvent) -> dict:
        return self.client.pages.update(notion_event.notion_id, **{
            "properties": {
                self.cfg.col_last_synced_time: {
                    "rich_text": [{
                        "text": {
                            "content": 'ERROR'
                        }
                    }]
                }
            }
        })
