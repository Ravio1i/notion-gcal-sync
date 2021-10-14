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
        cursor = None
        notion_event_items = []
        notion_event_count = 0
        while True:
            notion_event_res = self.query_items(delete, cursor=cursor)
            notion_event_count += len(notion_event_res['results'])
            print('Found {} events'.format(notion_event_count), end='\r')
            for i, obj in enumerate(notion_event_res['results']):
                notion_event = NotionEvent.from_api(obj, self.cfg)

                if not notion_event.time_start and self.cfg.no_date_action == 'skip':
                    logging.warning('Skipping event {} with no date specified'.format(notion_event.name))
                    continue

                if not notion_event.time_start and self.cfg.no_date_action == 'today':
                    logging.warning('Event {} with no date set to today'.format(notion_event.name))
                    notion_event.time_start = notion_event.time_end = date.today()

                notion_event_items.append(notion_event.dict_from_class())
            if not notion_event_res['has_more']:
                break
            cursor = notion_event_res['next_cursor']

        logging.info("Found {} event(s) in Notion".format(len(notion_event_items)))
        return notion_event_items

    def query_items(self, delete: bool = False, cursor: str = None):
        body = {
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
            }
        if cursor:
            body['start_cursor'] = cursor

        return self.client.databases.query(**body)

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
