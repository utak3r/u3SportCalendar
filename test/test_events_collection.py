import pytest
import datetime
from u3SportCalendar.Events import Event, EventsList, EventException

def test_event_creation():
    name = "test 1"
    start = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(hours=1)
    event = Event(name, start, end)
    assert event.name == name
    assert event.dateStart == start
    assert event.dateEnd == end

    event = Event()
    assert event.name == ""
    assert event.dateStart == None
    assert event.dateEnd == None

    end2 = datetime.datetime.now() + datetime.timedelta(hours=-1)
    with pytest.raises(EventException):
        event = Event(name, start, end2)

get_duration_test_data = [
    (datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1), 60 * 60),
    (None, None, 0)
]
@pytest.mark.parametrize("start, end, expected_duration", get_duration_test_data)
def test_get_duration(start, end, expected_duration):
    name = "test 1"
    event = Event(name, start, end)
    duration = event.get_duration()
    assert duration.seconds == expected_duration
