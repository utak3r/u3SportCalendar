import pytest
import datetime
import json
from u3SportCalendar.Events import Event, EventsList, EventException, EventsEncoder, EventsDecoder

def test_event_creation():
    name = "test 1"
    start = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(hours=1)
    event = Event(name, start, end)
    assert event.name() == name
    assert event.start() == start.replace(second=0).replace(microsecond=0).astimezone()
    assert event.end() == end.replace(second=0).replace(microsecond=0).astimezone()

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
    if (start is None):
        assert event.start() == start
    else:
        assert event.start() == start.replace(second=0).replace(microsecond=0).astimezone()
    if (end is None):
        assert event.end() == end
    else:
        assert event.end() == end.replace(second=0).replace(microsecond=0).astimezone()

def test_datetime_isoformat():
    name = "test 1"
    start = datetime.datetime(2025, 4, 16, 18, 28)
    end = datetime.datetime(2025, 4, 16, 19, 0)
    event = Event(name, start, end)
    assert event.start_as_iso() == "2025-04-16T18:28:00+02:00"
    assert event.end_as_iso() == "2025-04-16T19:00:00+02:00"

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

comparing_without_hour_test_data = [
    ("event 1", 2025, 4, 18, 19, 20, "event 2", 2025, 4, 18, 19, 20, False),
    ("event 1", 2025, 4, 18, 19, 20, "event 1", 2025, 4, 18, 19, 20, True),
    ("event 1", 2025, 4, 18, 19, 20, "event 1", 2025, 4, 18, 12, 0, True),
    ("event 1", 2025, 4, 18, 19, 20, "event 11", 2025, 4, 18, 12, 0, False),
]
@pytest.mark.parametrize("name1, year, month, day, hour, minute, " \
                         "name2, year2, month2, day2, hour2, minute2, " \
                         "expected_result", comparing_without_hour_test_data)
def test_comparing_without_hour(name1, year, month, day, hour, minute, 
                                name2, year2, month2, day2, hour2, minute2, 
                                expected_result
                                ):
    event1 = Event(name1, datetime.datetime(year, month, day, hour, minute))
    event2 = Event(name2, datetime.datetime(year2, month2, day2, hour2, minute2))
    assert event1.same_name_and_date_without_time(event2) == expected_result

def test_timezone_info():
    event = Event("test", datetime.datetime(2025, 4, 20, 18, 30), datetime.datetime(2025, 4, 20, 20, 00))
    event.get_timezone_info()

def test_list_add_get_count():
    events = EventsList()
    assert len(events) == 0
    events.add_event_params("test 1", datetime.datetime.now(), None)
    assert len(events) == 1
    events.add_event(Event("test 2", datetime.datetime.now(), None))
    assert len(events) == 2
    assert events[0].name() == "test 1"
    assert events[1].name() == "test 2"

def test_list_iterator():
    events = EventsList()
    events.add_event_params("test 1", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 2", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 3", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 4", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 5", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 6", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))

    assert len(events) == 6
    counter = 0
    for event in events:
        assert event.name() == events[counter].name()
        counter += 1
    assert counter == 6

def test_serialization():
    # Event
    single_event = Event(
        "test event two hours long", 
        datetime.datetime.now(), 
        datetime.datetime.now() + datetime.timedelta(hours=2)
        )
    event_serialized = json.dumps(single_event, cls=EventsEncoder)
    event_deserialized = json.loads(event_serialized, cls=EventsDecoder)
    assert single_event == event_deserialized

    # EventsList
    events = EventsList()
    events.add_event_params("test 1", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 2", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 3", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 4", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 5", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 6", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))

    events_serialized = json.dumps(events, cls=EventsEncoder)
    events_deserialized = json.loads(events_serialized, cls=EventsDecoder)
    assert len(events) == len(events_deserialized)
    assert events[0] == events_deserialized[0]
    assert events[1] == events_deserialized[1]
    assert events[2] == events_deserialized[2]
    assert events[3] == events_deserialized[3]
    assert events[4] == events_deserialized[4]
    assert events[5] == events_deserialized[5]

def test_lists_addition():
    events = EventsList()
    events.add_event_params("test 1", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 2", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 3", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))

    events_another = EventsList()
    events_another.add_event_params("test 4", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events_another.add_event_params("test 5", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events_another.add_event_params("test 6", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))

    events_joined = events + events_another
    assert len(events_joined) == len(events) + len(events_another)

    events_yet_another = EventsList()
    events.add_event_params("test 1", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 2", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    events.add_event_params("test 3", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=2))
    length = len(events_yet_another)
    events_yet_another += events_another
    assert len(events_yet_another) == length + len(events_another)

def test_trim_dates():
    events = EventsList()
    events.add_event_params("test 1", datetime.datetime.now() + datetime.timedelta(days=2), None)
    events.add_event_params("test 2", datetime.datetime.now() + datetime.timedelta(days=5), None)
    events.add_event_params("test 3", datetime.datetime.now() - datetime.timedelta(days=2), None)
    events.add_event_params("test 4", datetime.datetime.now() + datetime.timedelta(days=1), None)
    events.add_event_params("test 5", datetime.datetime.now() + datetime.timedelta(days=7), None)
    events.add_event_params("test 6", datetime.datetime.now() + datetime.timedelta(days=10), None)
    events.add_event_params("test 7", datetime.datetime.now() + datetime.timedelta(days=6), None)
    events.add_event_params("test 8", datetime.datetime.now() - datetime.timedelta(days=1), None)
    events.add_event_params("test 9", datetime.datetime.now() + datetime.timedelta(days=15), None)
    events.add_event_params("test 10", datetime.datetime.now() + datetime.timedelta(days=20), None)

    events_trimmed = events.trim_dates(0)
    assert len(events_trimmed) == 10

    events_trimmed = events.trim_dates(6)
    assert len(events_trimmed) == 4

    events_trimmed = events.trim_dates(8)
    assert len(events_trimmed) == 5

def test_prepare_updates_lists():
    existing_events = EventsList()
    existing_events.add_event(Event("Event 1", datetime.datetime(2025, 4, 20, 18, 30), datetime.datetime(2025, 4, 20, 20, 0)))
    existing_events.add_event(Event("Event 2", datetime.datetime(2025, 4, 22, 17, 0), datetime.datetime(2025, 4, 22, 19, 0)))
    existing_events.add_event(Event("Event 3", datetime.datetime(2025, 4, 25, 12, 15), datetime.datetime(2025, 4, 25, 13, 30)))
    existing_events.add_event(Event("Event 4", datetime.datetime(2025, 4, 28, 20, 0), datetime.datetime(2025, 4, 28, 21, 45)))
    existing_events.add_event(Event("Event 5", datetime.datetime(2025, 4, 30, 19, 45), datetime.datetime(2025, 4, 30, 21, 0)))

    newly_downloaded_events = EventsList()
    newly_downloaded_events.add_event(Event("Event 1", datetime.datetime(2025, 4, 20, 18, 30), datetime.datetime(2025, 4, 20, 20, 0)))
    newly_downloaded_events.add_event(Event("Event 6", datetime.datetime(2025, 5, 2, 20, 0), datetime.datetime(2025, 5, 2, 22, 0)))
    newly_downloaded_events.add_event(Event("Event 3", datetime.datetime(2025, 4, 25, 13, 0), datetime.datetime(2025, 4, 25, 15, 0)))
    newly_downloaded_events.add_event(Event("Event 7", datetime.datetime(2025, 5, 7, 15, 30), datetime.datetime(2025, 5, 7, 17, 0)))

    (tobe_removed, tobe_added) = existing_events.prepare_updates_lists(newly_downloaded_events, True)
    assert len(tobe_removed) == 1
    assert len(tobe_added) == 3
