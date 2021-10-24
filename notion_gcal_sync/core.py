import logging

import pandas as pd

from notion_gcal_sync.clients.GCalClient import GCalClient
from notion_gcal_sync.clients.NotionClient import NotionClient
from notion_gcal_sync.events.GCalEvent import GCalEvent
from notion_gcal_sync.events.NotionEvent import NotionEvent


def create_gcal_events(
    df: pd.DataFrame,
    gcal_client: GCalClient,
    notion_client: NotionClient,
    notion_df: pd.DataFrame,
    notion_specific_columns: list,
):
    logging.info("== CREATING EVENTS IN GCAL " + "=" * 73)
    # left only indicates that the events are only present in Notion
    notion_only_df = df.loc[df["_merge"] == "left_only"]
    # use notion_columns as columns for events to be created
    notion_only_df.columns = [
        x.replace("_notion", "") if any(k in x for k in notion_only_df.columns) else x for x in notion_only_df
    ]
    # drop all other columns
    notion_only_df = notion_only_df.loc[:, notion_df.columns]

    logging.info("Found {} event(s) to be created in Gcal".format(len(notion_only_df)))
    for idx, el in notion_only_df.iterrows():
        el["time_last_synced"] = notion_client.cfg.time.now()
        logging.info("- Creating event {} in GCal".format(el["name"]))
        gcal_event = GCalEvent(**el.drop(notion_specific_columns).to_dict(), cfg=gcal_client.cfg)
        gcal_event_res = gcal_client.create_event(gcal_event)

        logging.info("- Synchronize event {} in Notion".format(el["name"]))
        notion_event = NotionEvent(**el.to_dict(), cfg=notion_client.cfg)
        # Update values to make sure they are filled when not defined
        notion_event.gcal_event_id = gcal_event_res["id"]
        notion_event.gcal_page_url = gcal_event_res["htmlLink"]
        # Update on notion to be synchronized
        notion_event_res = notion_client.update_event(notion_event)
        if not notion_event_res:
            return
        gcal_event.gcal_event_id = gcal_event_res["id"]
        gcal_client.update_notion_link(gcal_event, notion_event_res["url"])


def create_notion_events(
    df: pd.DataFrame, gcal_client: GCalClient, notion_client: NotionClient, gcal_df: pd.DataFrame, gcal_specific_columns: list,
):
    logging.info("== CREATING EVENTS IN NOTION " + "=" * 71)
    # right only indicates that the events are only present in Notion
    gcal_only_df = df.loc[df["_merge"] == "right_only"]
    gcal_only_df.columns = [x.replace("_gcal", "") if any(k in x for k in gcal_only_df.columns) else x for x in gcal_only_df]
    gcal_only_df = gcal_only_df.loc[:, gcal_df.columns]
    logging.info("Found {} event(s) to be created in Notion".format(len(gcal_only_df)))
    for idx, el in gcal_only_df.iterrows():
        el["time_last_synced"] = gcal_client.cfg.time.now()
        logging.info('- Creating event "{}" in Notion'.format(el["name"]))
        notion_event = NotionEvent(**el.drop(gcal_specific_columns).to_dict(), cfg=notion_client.cfg)
        notion_event_res = notion_client.create_event(notion_event)

        logging.info('- Synchronize event "{}" in GCal'.format(el["name"]))
        gcal_event = GCalEvent(**el.to_dict(), cfg=gcal_client.cfg)
        gcal_event.notion_page_url = notion_client.cfg.notion_database_url + notion_event_res["id"].replace("-", "")
        gcal_event_res = gcal_client.update_event(gcal_event)
        if not gcal_event_res:
            return
        notion_event.notion_id = notion_event_res["id"]
        notion_client.update_gcal_link(notion_event, gcal_event_res["htmlLink"])


def update_events(
    df: pd.DataFrame,
    gcal_client: GCalClient,
    gcal_df: pd.DataFrame,
    gcal_specific_columns: list,
    notion_client: NotionClient,
    notion_df: pd.DataFrame,
    notion_specific_columns: list,
):
    logging.info("== UPDATING EVENTS " + "=" * 81)
    notion_values_df = df.loc[df["_merge"] == "both"]
    gcal_values_df = notion_values_df.copy()

    # Take these values if notion is newer
    notion_values_df.columns = [
        x.replace("_notion", "") if any(k in x for k in notion_values_df.columns) else x for x in notion_values_df
    ]
    notion_values_df = notion_values_df[notion_df.columns]

    # Take these values if gcal is newer
    gcal_values_df.columns = [
        x.replace("_gcal", "") if any(k in x for k in gcal_values_df.columns) else x for x in gcal_values_df
    ]
    gcal_values_df = gcal_values_df[gcal_df.columns]

    # Comparing the notion values to the gcal values
    diff_df = notion_values_df.drop(notion_specific_columns, axis=1).compare(
        gcal_values_df.drop(gcal_specific_columns, axis=1), keep_shape=True, keep_equal=False,
    )
    diff_df = diff_df.dropna(axis=0, how="all").astype(object).where(pd.notnull(diff_df), "")
    diff_df.to_csv("diff.csv")

    logging.info("Found {} event(s) to be updated".format(len(diff_df)))
    for idx, el in diff_df.iterrows():
        # Get the values from the notion values
        gcal_updates = gcal_values_df.iloc[idx]
        # Nothing is newer but somewhere this is a difference
        if gcal_updates["read_only"] == "True":
            logging.info("Skipping read only event {} with update".format(gcal_updates["name"]))
            continue

        notion_updates = notion_values_df.iloc[idx]
        if not el["time_last_updated"]["self"] or not el["time_last_updated"]["other"]:
            logging.error('The event "{}" is synced, but still there is a difference'.format(notion_updates["name"]))
            logging.error(el.loc[:, ~el.isin([""])].to_dict())
            notion_event = NotionEvent(**notion_updates.to_dict(), cfg=notion_client.cfg)
            logging.error("Setting sync status to ERROR")
            notion_client.set_sync_error(notion_event)
            continue

        notion_last_updated = notion_client.cfg.time.to_datetime(el["time_last_updated"]["self"])
        gcal_last_updated = gcal_client.cfg.time.to_datetime(el["time_last_updated"]["other"])

        # Notion is newer
        if notion_last_updated > gcal_last_updated:
            notion_updates["time_last_synced"] = notion_client.cfg.time.now()
            logging.info('Event "{}" has an update in Notion'.format(notion_updates["name"]))
            # Use values from notion and drop notion specific columns
            logging.info('- Updating event "{}" in GCal'.format(notion_updates["name"]))
            gcal_event = GCalEvent(**notion_updates.drop(notion_specific_columns).to_dict(), cfg=gcal_client.cfg)
            gcal_event_res = gcal_client.update_event(gcal_event)
            if not gcal_event_res:
                continue

            logging.info('- Synchronize event "{}" in Notion'.format(notion_updates["name"]))
            notion_event = NotionEvent(**notion_updates.to_dict(), cfg=notion_client.cfg)
            notion_event.gcal_page_url = gcal_event_res["htmlLink"] + "&ctz=" + notion_client.cfg.time.timezone_name
            notion_event_res = notion_client.update_event(notion_event)
            if not notion_event_res:
                continue
            gcal_event.gcal_event_id = gcal_event_res["id"]
            gcal_client.update_notion_link(gcal_event, notion_event_res["url"])

        # GCal is newer
        if notion_last_updated < gcal_last_updated:
            gcal_updates["time_last_synced"] = gcal_client.cfg.time.now()

            logging.info('Event "{}" has an update in GCal'.format(gcal_updates["name"]))
            logging.info('- Updating event "{}" in Notion'.format(gcal_updates["name"]))
            notion_event = NotionEvent(
                **gcal_updates.drop(gcal_specific_columns).to_dict(),
                notion_id=notion_updates["notion_id"],
                cfg=notion_client.cfg,
            )
            notion_event_res = notion_client.update_event(notion_event)
            if not notion_event_res:
                continue

            logging.info('- Synchronize event "{}" in GCal'.format(gcal_updates["name"]))
            gcal_event = GCalEvent(**gcal_updates.to_dict(), cfg=gcal_client.cfg)
            gcal_event.notion_page_url = notion_event_res["url"]
            gcal_event_res = gcal_client.update_event(gcal_event)
            if not gcal_event_res:
                continue
            notion_client.update_gcal_link(notion_event, gcal_event_res["htmlLink"])


def delete_gcal_events(notion_client: NotionClient, gcal_client: GCalClient, notion_specific_columns: list):
    logging.info("== DELETING EVENTS IN GCAL " + "=" * 73)
    notion_events_delete = notion_client.list_events(delete=True)
    notion_events_delete_df = pd.DataFrame(notion_events_delete).astype(str)
    for idx, el in notion_events_delete_df.iterrows():
        logging.info('- Deleting event "{}" in GCal'.format(el["name"]))

        gcal_event = GCalEvent(**el.drop(notion_specific_columns).to_dict(), cfg=gcal_client.cfg)
        gcal_event_res = gcal_client.get_event(gcal_event.gcal_calendar_id, gcal_event.gcal_event_id)
        if not gcal_event_res.get("status"):
            logging.warning("- Event {} never existed in GCal".format(el["name"]))
        elif gcal_event_res["status"] == "cancelled":
            logging.warning("- Event {} already deleted in GCal".format(el["name"]))
        else:
            gcal_client.delete_event(gcal_event)

        logging.info('- Put event "{}" in Notion as deleted'.format(el["name"]))
        notion_event = NotionEvent(**el.to_dict(), cfg=notion_client.cfg)
        notion_client.delete_event(notion_event)


def sync(cfg):
    logging.info("=" * 100)
    ###########################################################################
    # Fetching Notion Events
    ###########################################################################
    logging.info("== FETCHING EVENTS " + "=" * 81)
    logging.info("Fetching events from Notion")
    notion_client = NotionClient(cfg)
    notion_events = notion_client.list_events()
    notion_df = pd.DataFrame(notion_events).astype(str)

    ###########################################################################
    # Fetching GCal Events
    ###########################################################################
    logging.info("Fetching events from Google Calendar")
    gcal_client = GCalClient(cfg)
    gcal_events = sum([gcal_client.list_events(cfg.gcal_calendars[calendar]) for calendar in cfg.gcal_calendars], [],)
    gcal_df = pd.DataFrame(gcal_events).astype(str)

    ###########################################################################
    # Creating Dataframe with all information
    ###########################################################################
    df = None
    if not notion_df.empty and not gcal_df.empty:
        df = notion_df.merge(
            gcal_df, on="gcal_event_id", how="outer", indicator=True, suffixes=("_notion", "_gcal"),
        ).drop_duplicates()
    # TODO: MAKE THIS BOOTSTRAP AUTOMATIC ITS UGLY
    elif gcal_df.empty and not notion_df.empty:
        df = notion_df.copy()
        df["color_id"] = ""
        gcal_df = pd.DataFrame(columns=df.columns).drop(["notion_id"])
        df["_merge"] = "left_only"
    elif notion_df.empty and not gcal_df.empty:
        df = gcal_df.copy()
        df["notion_id"] = ""
        notion_df = pd.DataFrame(columns=df.columns).drop(columns=["color_id"])
        df["_merge"] = "right_only"
    else:
        logging.error("Both GCal and Notion are empty. Exiting...")
        exit()

    # Remove null objects from dataframe
    df = df.astype(object).where(pd.notnull(df), "")
    notion_specific_columns = list(set(notion_df.columns) - set(gcal_df.columns))
    gcal_specific_columns = list(set(gcal_df.columns) - set(notion_df.columns))

    ###########################################################################
    # SYNCING
    ###########################################################################
    # Notion events not in GCAL
    create_gcal_events(df, gcal_client, notion_client, notion_df, notion_specific_columns)
    # GCAL events not in Notion Events
    create_notion_events(df, gcal_client, notion_client, gcal_df, gcal_specific_columns)
    # GCAL or Notion events requiring update
    update_events(
        df, gcal_client, gcal_df, gcal_specific_columns, notion_client, notion_df, notion_specific_columns,
    )
    # GCAL events to be deleted
    delete_gcal_events(notion_client, gcal_client, notion_specific_columns)
