# Notion-GCal-Sync

## Setup

### Google calendar

1. Create credentials like [this](https://developers.google.com/workspace/guides/create-credentials).
2. Download credentials and copy them into this folder as `client_secret.json`.

    ```bash
    mv client_secret_*.apps.googleusercontent.com.json client_secret.json
    ```

The `token.json` will store the user's access and refresh tokens as json and is created automatically when the authorization flow completes for the first time.

**NOTE:** Keep the order of the config.yml and dont remove the entries!

## Usage

NOTE: this will update your sources in gcal. If you want your old links dont run this script dude!

NOTE: This will also update all your invites from other calendars not specified to your default one