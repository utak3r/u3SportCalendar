import datetime
import json
from json import JSONEncoder, JSONDecoder

class EventException(Exception):
    def __init__(self, msg):
        self.msg = msg
        print('EventException exception occured')


class EventsEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                "__class__": "datetime",
                "y": obj.year,
                "month": obj.month,
                "d": obj.day,
                "h": obj.hour,
                "minute": obj.minute,
                "s": obj.second 
            }
        if (isinstance(obj, Event)):
            return {
                "__class__": "Event",
                "name": obj.name(),
                "start": obj.start(),
                "end": obj.end()
            }
        if (isinstance(obj, EventsList)):
            return {
                "__class__": "EventsList",
                "events": obj.the_list
            }
        return JSONEncoder.default(self, obj)

class EventsDecoder(JSONDecoder):
    def __init__(self):
        JSONDecoder.__init__(self, object_hook=EventsDecoder.from_dict)

    @staticmethod
    def from_dict(dict):
        if dict.get("__class__") == "datetime":
            return datetime.datetime(
                dict["y"], dict["month"], dict["d"],
                dict["h"], dict["minute"], dict["s"]
                )
        if dict.get("__class__") == "Event":
            return Event(
                name=dict["name"], start=dict["start"], end=dict["end"]
            )
        if dict.get("__class__") == "EventsList":
            lista = EventsList()
            lista.the_list = dict["events"]
            return lista
        return dict


class Event():
    def __init__(self, name:str="", start:datetime.datetime=None, end:datetime.datetime=None):
        self.the_name = name
        self.the_start = None
        if (start is not None):
            self.the_start = start.replace(second=0).replace(microsecond=0)
        self.the_end = None
        if (end is not None):
            self.the_end = end.replace(second=0).replace(microsecond=0)
        if (start is not None and end is not None):
            if (end < start):
                self.the_end = start.replace(second=0).replace(microsecond=0)
                raise EventException("End date is sooner than start date.")
            
    def toJson(self) -> str:
        return json.dumps(self, cls=EventsEncoder)
    
    @classmethod
    def fromJson(cls, serialized):
        return json.loads(serialized, cls=EventsDecoder)
    
    def name(self) -> str:
        return self.the_name
    
    def start(self) -> datetime.datetime:
        return self.the_start
    
    def start_iso(self) -> str:
        return self.the_start.isoformat(timespec='seconds')
    
    def end(self) -> datetime.datetime:
        return self.the_end

    def end_iso(self) -> str:
        return self.the_end.isoformat(timespec='seconds')

    def duration(self) -> datetime.timedelta:
        duration = datetime.timedelta()
        if (self.the_start is not None and self.the_end is not None):
            duration = self.the_end - self.the_start
        return duration
    
    def __str__(self):
        return self.get_as_text()
    
    def __eq__(self, other):
        return (
            self.name() == other.name() and
            self.start() == other.start() and
            self.end() == other.end()
        )
    
    def __gt__(self, other):
        return (self.start() > other.start())
    
    def __lt__(self, other):
        return (self.start() < other.start())

    def get_as_text(self) -> str:
        text = ""
        if (self.the_name != ""):
            text += self.the_name
        dates_text = ""
        if (self.the_start is not None):
            dates_text += self.the_start.strftime("%Y-%m-%d, %H:%M")
        if (self.the_end is not None):
            dates_text += self.the_end.strftime(" - %Y-%m-%d, %H:%M")
        if (dates_text != ""):
            text += " (" + dates_text + ")"
        return text
    

class EventsList:
    def __init__(self):
        self.the_list = []
        self.iter_counter = 0

    def __getitem__(self, key) -> Event:
        return self.the_list[key]

    def add_event_params(self, name, start, end):
        event = Event(name, start, end)
        self.the_list.append(event)
    
    def add_event(self, event: Event):
        if (event is not None):
            self.the_list.append(event)

    def toJson(self) -> str:
        return json.dumps(self, cls=EventsEncoder)

    @classmethod
    def fromJson(cls, serialized):
        return json.loads(serialized, cls=EventsDecoder)

    def __len__(self):
        return len(self.the_list)
    
    def __iter__(self):
        self.iter_counter = 0
        return self
    
    def __next__(self):
        if (self.iter_counter < len(self.the_list)):
            ret = self.the_list[self.iter_counter]
            self.iter_counter += 1
            return ret
        else:
            raise StopIteration

