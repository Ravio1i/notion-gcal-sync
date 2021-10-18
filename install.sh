#!/bin/bash

CONFIG_FILE="notion_gcal_sync/config.yml"
CLIENT_CREDENTIALS="notion_gcal_sync/client_credentials.json"
CLIENT_TOKEN="notion_gcal_sync/token.json"

pip install .

NOTION_GCAL_SYNC_LIB="$(pip list -v | grep notion-gcal-sync | awk '{print $3}')/notion_gcal_sync"
cp $CONFIG_FILE "$NOTION_GCAL_SYNC_LIB/config.yml"
cp $CLIENT_CREDENTIALS "$NOTION_GCAL_SYNC_LIB/client_credentials.json"
cp $CLIENT_TOKEN "$NOTION_GCAL_SYNC_LIB/token.json"
