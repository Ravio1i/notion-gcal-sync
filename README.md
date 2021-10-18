[![Unit Tests](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/test.yml/badge.svg)](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/test.yml)
# Notion-GCal-Sync

Notion-GCal-Sync is a python application to bidirectional synchronize calendar events within notion and google calendar.

## Setup 

From pip and running directly

```bash
pip install notion-gcal-sync
```

With docker (Not the mounting of `client_secret.json` and `config.yml`)

```yaml 
docker pull notion-gcal-sync
```

Keep following [these instructions](docs/setup.md).

## Usage

**IMPORTANT:** Make sure you followed the [setup](docs/setup.md) and configured the `config.yml` with your notion token and page for Notion API and gathered and setup credentials `client_secret.json` for Google Calendar API.

From pip and running directly

```bash
notion-gcal-sync
```

With docker (Not the mounting of `client_secret.json` and `config.yml`)

```yaml
docker run --net=host -it \
    -v $(pwd)/config.yml:/app/notion_gcal_sync/config.yml \
    -v $(pwd)/client_credentials.json:/app/notion_gcal_sync/client_credentials.json \
    notion-gcal-sync
```

On first run or when token is old you will be asked to authorize the application. Follow the link and authorize with your account. After authorization the application will continue.

```bash
$ notion-gcal-sync
...
Please visit this URL to authorize this application: 
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=***
```


## Notes

BE AWARE OF THE FOLLOWING:
* This sync will update your source links in gcal. Links to mail etc. will get overwritten with a link to the notion page.
  The original links will be put on top of the description
* This sync will update all your invites from other calendars not specified to your default calendar. There is a button on gcal to restore 
  back
* Goals defined from calendar apps are skipped.
* Recurrent original events are skipped. Recurrent occurrences of events are created one by one in notion. 
  Changing in notion will change only an occurrence in GCal.


## Notes

With around ~2500 events in gcal the sync:
* to get all events took ~1min