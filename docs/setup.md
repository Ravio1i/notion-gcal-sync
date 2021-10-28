# Setup notion-gcal-sync

This document describes how to set up and configure your notion-gcal-sync.

## Installation

With [pip](https://pypi.org/project/notion-gcal-sync/)

```bash
pip install notion-gcal-sync
```

With [docker](https://github.com/Ravio1i/notion-gcal-sync/pkgs/container/notion-gcal-sync)

```yaml
docker pull ghrc.io/ravio1i/notion-gcal-sync
```

## Configuration

Additionally, to installing the python package you will need to properly configure and authenticate.
This requires the 2 files in your user home `~/.notion-gcal-sync` (`C:\Users\dude\.notion-gcal-sync`)

* `config.yml`
* `client_secret.yml`

The default `config.yml` is included in the installation and can be found in the repo root. If no `config.yml` exists in the `~/.notion-gcal-sync` folder you'll be prompted on the next run of the application.
## Setup credentials for Google Calendar

The following is a summary of [this](https://developers.google.com/workspace/guides/create-credentials) and will get you the
credentials for authenticating against your Google calendar.

1. New Project and call it something e.g `notion`. (Note: Make sure to select the newly created project)
2. Navigate to the [API Library](https://console.cloud.google.com/apis/).
3. Search for `Google Calendar API` and `Enable`.
4. Navigate to the [API Credentials Page](https://console.cloud.google.com/apis/credentials).
5. Click `+ Create Credentials` > `OAuth client ID`
6. If Consent Screen > `CONFIGURE CONSENT SCREEN`
    1. OAuth consent Screen
        1. Set User Type to `External`
        2. For App information use any App name, like `notion-gcal-sync` and for support email use your email.
        3. For Developer contact information use your email as well.
        4. `Save and continue`
    2. Scopes
        1. Click `Add or Remove Scopes`
        2. Select `Google Calendar API` with Scope `.../auth/calendar` and click `Update`
        3. `Save and Continue`
    3. Test users
        1. `+ Add users` and add your email
        2. `Save and continue` (The error `Ineligible accounts not added` can be ignored)
7. Navigate to the [API Credentials Page](https://console.cloud.google.com/apis/credentials).
8. Click `+ Create Credentials` > `OAuth client ID`
    1. Select `Desktop App` with any name, like `notion-gcal-sync`
    2. `Create`
    3. In the new prompt `DOWNLOAD JSON` or on the just created credentials on `Actions` click the `Download OAuth client`
       icon.

The `token.json` will store the user's access and refresh tokens as json and is created automatically when the authorization
flow completes for the first time.

## Setup credentials for Notion

The following is a summary of [this](https://developers.notion.com/docs/authorization) and will set up your notion integration
to authenticate this application for notion.

1. Navigate to [Notion Integrations](https://www.notion.so/my-integrations).
2. Click `Create new integration` and give it name, like `notion-gcal-sync`.
3. On the page of the integration copy the contents of your `Internal Integration Token`.


### Set up your Notion page

1. Duplicate [this page](https://virtuose.notion.site/130c26a74ca44da585506be9e8af678d?v=f76cc35334204f5abf0cd749134dc047) to
   your notion.

   Don't be overwhelmed by the amount of properties. You can hide or [rename columns](#Columns) you don't want to see, **but do
   not remove them!**

2. Click `Share` in the top right corner of your duplicated page and `Invite`
   your [Notion Integration](#setup-credentials-for-notion) with `Can edit` .

## Integrate your google calendars

1. Navigate to [Google Calendar](https://calendar.google.com) and go to Settings.
2. Click on your calendar you want to have synced with notion. and click `Integrate Calendar`
3. Copy the `Calendar-ID`
    1. For your default calendar this is something like `***@gmail.com`
    2. For other calendars this is something like: `***@group.calendar.google.com`
4. Add the `Calendar-ID` to your `config.yml` and specify your default calendar as `default_calendar_id`.

   Add any amount of additional calendars to the `calendars`. Make sure your default calendar is specified in the calendars
   section as well.
    ```yaml
   ...
    gcal:
      default_calendar_id: ***@gmail.com
      default_calendar_name: Default
      calendars:
        Default: ***@gmail.com
        Some Other Calendar: '***@group.calendar.google.com'
       ```

### Columns


* `Name (text)`: The name (summary) of an event.
* `Date (date)`: The date of the event. If nothing is specified the `no_date_action` will be used.
* `Description: (text)`: The description of the event.
* `Location: (text)`: Location field, e.g. place in Google Maps.
* `Calendar (select)`: The Name of the calendar specified as a key in `calendars` section.
* `Delete? (checkbox)`: If you select this, the event will be removed from Google Calendar and the `Deleted` column will be
  set.
* `Delete (checkbox) [Automatic]`:  Indicates whether an event got deleted from Google Calendar.
* `Read Only (checkbox) (Automatic)`: This gets selected automatically by events which are from other calendars than yours.
  This is for example if you accept a meeting from someone. Because you cannot change this event this is marked as read only.
* `GCal event url (url) [Automatic]`: Link to your Google Calendar event.
* `GCal Recurrence (text) [Automatic]`: If specified, indicates the url of the event with recurrence in Google Calendar.
  Changing an event with recurrence will only change one occurrence.
* `GCal Calendar Id (select) [Automatic]`: The Calendar id. One of the calendar ids specified in calendar section.
* `Last Updated (last_edited_time) [Automatic]`: Indicates if you changed something in notion.
* `Last Synced (text) [Automatic]`: Indicates as timestamp as text when the last sync changed a row.

## Other Configurations

**NOTE:** Keep the order of the config.yml and don't remove the entries!

* `no_date_action`: What to do with items that don't have a date. Defaults to `skip`.
    * `skip`: Won't sync this item
    * `today`: Updates the items `date` to today's date and synchronizes.
