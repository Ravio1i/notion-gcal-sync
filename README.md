[![CI](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/notion-gcal-sync.svg)](https://badge.fury.io/py/notion-gcal-sync)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Notion-GCal-Sync

Notion-GCal-Sync is a python application to bidirectional synchronize calendar events within notion and google calendar.

## Getting started

1. Install package from [PyPi](https://pypi.org/project/notion-gcal-sync/)

    ```bash
    pip install notion-gcal-sync
    ```

2. Get your Google Calendar `credentials.json` [like this](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-credentials-for-google-calendar)
3. Get your Notion Token [like this](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-credentials-for-notion)
4. Set up the Notion page [like this]((https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-up-your-notion-page))
5. Create config folder `~/.notion-gcal-sync` and copy the `credentials.json` inside

    **Linux (or WSL)**
    ```bash
    cp ~/Downloads/client_secret_*.apps.googleusercontent.com.json "~/.notion-gcal-sync/client_secret.json"
    ```

    **Windows**
    Copy your `client_secret_*.apps.googleusercontent.com.json` as `client_secret.json` inside `C:\Users\dude\.notion-gcal-sync`
    ```powershell
    # TODO
    ```


6. Run the script and fill out the prompts. If not sure skip the optional bits.
   1. Make [sure you get your timezone right](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
      1. Use your TZ database name as `timezone_name`
      2. Use the UTC DST offset as `timezone_diff`
   2. `google_mail`: Your mail you are using in google calendar want to have synced
   3. `notion_database_url` The url for the page you set up in 4.
   4. `notion_token`: The token you set up in 3.

    ```bash
    notion-gcal-sync

    2021-10-28 19:55:41,198 [INFO] /home/worker/.notion-gcal-sync/config.yml does not exist
    Create non-existing /home/worker/.notion-gcal-sync/config.yml? [Y/n]: y
    2021-10-28 19:55:42,630 [INFO] Configuring /home/worker/.notion-gcal-sync/config.yml
    default_event_length [60]:
    no_date_action [skip]:
    timezone_name [Europe/Berlin]:
    timezone_diff [+02:00]:
    google_mail (e.g name@gmail.com): cooldude@gmail.com
    notion_database_url [https://www.notion.so/***?v=***&p=]:
    notion_token: secret_ASDFASDFCASDF
    ```

7. It will prompt you to authenticate yourself for google. This will create a `token.json`.

    ```bash
    $ notion-gcal-sync
    ...
    Please visit this URL to authorize this application:
    https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=***
    ```

For more information follow [these instructions](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md).

## Usage

Make sure you followed the [setup](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md) and
configured the `config.yml` with your notion token and page for Notion API and gathered and setup
credentials `client_secret.json` for Google Calendar API.

```bash
notion-gcal-sync
```

### Docker
To run inside the container you need to add the volume at `~/.notion-gcal-sync`

```yaml
docker run -v ~/.notion-gcal-sync:/home/worker/.notion-gcal-sync notion-gcal-sync
```


If you want to update the setup within the cli or only map the credentials, you'll need to add interactive mode `-it` and for authenticating a new token you'll also need `--net=host`

```yaml
docker run --net=host -it \
     -v ~/.notion-gcal-sync/client_secret.json:/home/worker/notion-gcal-sync/client_secret.json \
     notion-gcal-sync
```

If you do not want to mount, build it yourself with your credentials.

```Dockerfile
FROM ghrc.io/ravio1i/notion-gcal-sync
COPY token.json /home/worker/token.json
COPY config.yml /home/worker/config.json
```

## Notes

BE AWARE OF THE FOLLOWING:

* This sync will update your source links in gcal. Links to mail etc. will get overwritten with a link to the notion page. The
  original links will be put on top of the description
* This sync will update all your invites from other calendars not specified to your default calendar. There is a button on gcal
  to restore back
* Goals defined from calendar apps are skipped.
* Recurrent original events are skipped. Recurrent occurrences of events are created one by one in notion. Changing in notion
  will change only an occurrence in GCal.

With around ~2500 events in gcal the sync:

* to get all events took ~1min
