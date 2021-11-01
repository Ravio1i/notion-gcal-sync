import pytest


@pytest.fixture
def gcal_event_obj():
    return {"id": "abc123", "summary": "title", "organizer": {}}


def test_from_api():
    pass


# def test_get_meta():
#     assert False
#
#
# def test_get_time():
#     assert False
#
#
# def test_get_calendar():
#     assert False
#
#
# def test_get_recurrent_event():
#     assert False
#
#
# def test_body():
#     assert False
