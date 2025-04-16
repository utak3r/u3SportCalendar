import pytest
import datetime
from u3SportCalendar.Events import Event, EventsList, EventException

def test_event_creation():
    name = "test 1"
    start = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(hours=1)
    event = Event(name, start, end)
    assert event.name() == name
    assert event.start() == start
    assert event.end() == end

    event = Event()
    assert event.name() == ""
    assert event.start() == None
    assert event.end() == None

    end2 = datetime.datetime.now() + datetime.timedelta(hours=-1)
    with pytest.raises(EventException):
        event = Event(name, start, end2)

get_duration_test_data = [
    (datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1), 60 * 60),
    (None, None, 0)
]
@pytest.mark.parametrize("start, end, expected_duration", get_duration_test_data)
def test_duration(start, end, expected_duration):
    name = "test 1"
    event = Event(name, start, end)
    duration = event.duration()
    assert duration.seconds == expected_duration

simple_getters_test_data = [
    ("test 1", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1)),
    ("test 2", None, None),
    ("", None, None)
]
@pytest.mark.parametrize("name, start, end", simple_getters_test_data)
def test_simple_getters(name, start, end):
    event = Event(name, start, end)
    assert event.name() == name
    assert event.start() == start
    assert event.end() == end

def test_datetime_isoformat():
    name = "test 1"
    start = datetime.datetime(2025, 4, 16, 18, 28)
    end = datetime.datetime(2025, 4, 16, 19, 0)
    event = Event(name, start, end)
    assert event.start_iso() == "2025-04-16T18:28:00"
    assert event.end_iso() == "2025-04-16T19:00:00"

get_as_text_test_data = [
    ("test 1", 2025, 4, 16, 18, 28, 2025, 4, 16, 19, 0, "test 1 (2025-04-16, 18:28 - 2025-04-16, 19:00)"),
    ("test 2", 2025, 4, 16, 18, 28, 0, 4, 16, 19, 0, "test 2 (2025-04-16, 18:28)"),
    ("test 3", 0, 4, 16, 18, 28, 2025, 4, 16, 19, 0, "test 3 ( - 2025-04-16, 19:00)"),
    ("test 4", 0, 4, 16, 18, 28, 0, 4, 16, 19, 0, "test 4"),
]
@pytest.mark.parametrize("name, " \
    "start_year, start_month, start_day, start_hour, start_minute, " \
    "end_year, end_month, end_day, end_hour, end_minute," \
    "expected_string", get_as_text_test_data)
def test_get_as_text(name, 
                     start_year, start_month, start_day, start_hour, start_minute,
                     end_year, end_month, end_day, end_hour, end_minute,
                     expected_string):
    name = name
    start = None
    end = None
    if (start_year > 0):
        start = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute)
    if (end_year > 0):
        end = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute)
    event = Event(name, start, end)
    assert event.get_as_text() == expected_string
