# Notion-GCal-Sync

## Setup

### Google calendar

1. Create credentials like [this](https://developers.google.com/workspace/guides/create-credentials).
2. Download credentials and copy them into this folder as `client_secret.json`.

    ```bash
    mv client_secret_*.apps.googleusercontent.com.json client_secret.json
    ```

The `token.json` will store the user's access and refresh tokens as json and is created automatically when the authorization flow completes for the first time.

**NOTE:** Keep the order of the config.yml and don't remove the entries!

## Usage

BE AWARE OF THE FOLLOWING:
* This sync will update your source links in gcal. Links to mails etc. will get overwritten with a link to the notion page.
  The original links will be put on top of the description
* This sync will update all your invites from other calendars not specified to your default calendar. There is a button on gcal to restore 
  back
* Goals defined from calendar apps are skipped.
* Recurrent original events are skipped. Recurrent occurrences of events are created one by one in notion. 
  Changing in notion will change only an occurrence in GCal.