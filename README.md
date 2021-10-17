[![Unit Tests](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/test.yml/badge.svg)](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/test.yml)
# Notion-GCal-Sync



## Setup 

From pip and running directly 
```bash
pip install notion-gcal-sync
```

With docker (Not the mounting of `client_secret.json` and `config.yml`)
```yaml
docker pull notion-gcal-sync
```

**!!! Do not run it yet because your credentials are obviously not yet set up !!!**

Keep following the instructions 

### Credentials for Google Calendar

The following is a summary of [this](https://developers.google.com/workspace/guides/create-credentials) and will get you the credentials for authenticating against your Google calendar.

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
   3. In the new prompt `DOWNLOAD JSON` or on the just created credentials on `Actions` click the `Download OAuth client` icon.

The `token.json` will store the user's access and refresh tokens as json and is created automatically when the authorization flow completes for the first time.

10. **IF INSTALLED WITH PIP:** Move your credentials into this folder as `client_secret.json`.
    
    Linux (or WSL):
    ```bash
    NOTION_GCAL_SYNC_LIB="$(pip list -v | grep notion-gcal-sync | awk '{print $3}')/notion_gcal_sync"
    cp client_secret_*.apps.googleusercontent.com.json "$NOTION_GCAL_SYNC_LIB/client_secret.json"
    ```
    
    Windows: Search where your Python library got installed and copy your `client_secret_*.apps.googleusercontent.com.json` as `client_secret.json`. inside
    ```powershell
    # TODO
    ```

### Credentials for Notion

The following is a summary of [this](https://developers.notion.com/docs/authorization) and will set up your notion integration to authenticate this application for notion.

1. Navigate to [Notion Integrations](https://www.notion.so/my-integrations).
2. Click `Create new integration` and give it name, like `notion-gcal-sync`.
3. On the page of the integration copy the contents of your `Internal Integration Token`.
4. Insert your token data in your `config.yml`:
   ```yaml
   ...
   notion:
      ...
      token: '***'
   ```

### Set up your Notion page

1. Duplicate [this page](https://virtuose.notion.site/130c26a74ca44da585506be9e8af678d?v=f76cc35334204f5abf0cd749134dc047) to your notion. 

    Don't be overwhelmed by the amount of properties. You can hide or [rename columns](#Columns) you don't want to see, **but do not remove them!**

2. Click `Share` in the top right corner of your duplicated page and `Invite` your [Notion Integration](#credentials-for-notion) with `Can edit` .

3. Copy the URL of your duplicated page and add it to your `config.yml`. 
   
   **Append a `&p=` to the URL.**

    ```yaml
   ...
   notion:
      notion_url: https://www.notion.so/[subdomain]/***?v=***&p=
      token: '***'
   ```

### Integrate your google calendars

1. Navigate to [Google Calendar](https://calendar.google.com) and go to Settings.
2. Click on your calendar you want to have synced with notion. and click `Integrate Calendar`
3. Copy the `Calendar-ID`
   1. For your default calendar this is something like `***@gmail.com`
   2. For other calendars this is something like: `***@group.calendar.google.com`
4. Add the `Calendar-ID` to your `config.yml` and specify your default calendar as `default_calendar_id`.

   Add any amount of additional calendars to the `calendars`.
   Make sure your default calendar is specified in the calendars section as well.
    ```yaml
   ...
    gcal:
      default_calendar_id: ***@gmail.com
      default_calendar_name: Default
      calendars:
        Default: ***@gmail.com
        Some Other Calendar: '***@group.calendar.google.com'
       ```

## Configure

**NOTE:** Keep the order of the config.yml and don't remove the entries!

* `no_date_action`: What to do with items that don't have a date. Defaults to `skip`.
    * `skip`: Won't sync this item
    * `today`: Updates the items `date` to today's date and synchronizes.

### Columns

* `Name`: The name (summary) of an event.
* `Date`: The date of the event. If nothing is specified the `no_date_action` will be used

## Usage

**IMPORTANT:** Make sure you followed the setup and configured `config.yml` with your [notion token and page](#credentials-for-notion) for Notion API and [gathered and setup credentials](#credentials-for-google-calendar)  `client_secret.json` for Google Calendar API.

From pip and running directly 
```bash
notion-gcal-sync
```

With docker (Not the mounting of `client_secret.json` and `config.yml`)
```yaml
docker run -v client_secret.json:client_secret.json -v config.yml:config.yml notion-gcal-sync
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