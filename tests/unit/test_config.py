import pytest

from notion_gcal_sync.config import Config


def test_empty_config():
    assert Config()


@pytest.mark.parametrize(
    "test_url, expected",
    [
        ("https://www.notion.so/subdomain/THE_ID?v=asdfasdf123&p=", "THE_ID"),
        ("https://www.notion.so/THE_ID?v=asdfasdf123&p=", "THE_ID"),
        ("https://www.notion.so/THE_ID?v=asdfasdf123", "THE_ID"),
        ("https://www.notion.so/THE_ID?v=", None),
        ("https://www.notion.so/THE_ID", None),
        ("https://www.notion.so/THE_ID&p=", None),
        ("http://www.notion.so/THE_ID?v=asdfasdf123&p=", None),
        (None, None),
    ],
)
def test_database_id(time_fixture, notion_columns_fixture, test_url, expected):
    config = Config(
        default_event_length=60,
        no_date_action="skip",
        gcal_calendars={"Default": "dude@gmail.com"},
        gcal_default_calendar_name="Default",
        notion_database_url=test_url,
        notion_token="SECRET",
        notion_columns=notion_columns_fixture,
        timezone_name="Europe/Berlin",
    )
    assert config.notion_database_id == expected


def test_default_event_length(config_fixture):
    config_fixture.default_event_length = "123"
    assert config_fixture.default_event_length == 60


@pytest.mark.parametrize(
    "test_action, expected",
    [("skip", "skip"), ("today", "today"), ("something_else", "skip")],
)
def test_no_date_action(config_fixture, test_action, expected):
    config_fixture.no_date_action = test_action
    assert config_fixture.no_date_action == expected


@pytest.mark.parametrize(
    "test_calendar_id, expected",
    [
        ("dude@gmail.com", "Default"),
        ("abc123@group.calendar.google.com", "Calendar2"),
        ("error@group.calendar.google.com", None),
        (None, None),
    ],
)
def test_get_calendar_name(config_fixture, test_calendar_id, expected):
    assert config_fixture.get_calendar_name(test_calendar_id) == expected


def test_notion_invalid_columns(notion_columns_fixture):
    del notion_columns_fixture["name"]
    with pytest.raises(ValueError):
        Config(notion_columns=notion_columns_fixture)


@pytest.mark.parametrize(
    "test_calendar_name, expected",
    [
        ("Default", "dude@gmail.com"),
        ("Calendar2", "abc123@group.calendar.google.com"),
        ("error@group.calendar.google.com", None),
        (None, None),
    ],
)
def test_get_calendar_id(config_fixture, test_calendar_name, expected):
    assert config_fixture.get_calendar_id(test_calendar_name) == expected


@pytest.mark.parametrize(
    "test_calendar_id, expected",
    [
        ("dude@gmail.com", True),
        ("abc123@group.calendar.google.com", True),
        ("error@group.calendar.google.com", False),
        (None, False),
    ],
)
def test_is_valid_calendar_id(config_fixture, test_calendar_id, expected):
    assert config_fixture.is_valid_calendar_id(test_calendar_id) == expected


@pytest.mark.parametrize(
    "test_calendar_name, expected",
    [("Default", True), ("Calendar2", True), ("error@group.calendar.google.com", False), (None, False)],
)
def test_is_valid_calendar_name(config_fixture, test_calendar_name, expected):
    assert config_fixture.is_valid_calendar_name(test_calendar_name) == expected


def test_to_dict(config_fixture, config_dict_fixture):
    assert config_fixture.to_dict() == config_dict_fixture
