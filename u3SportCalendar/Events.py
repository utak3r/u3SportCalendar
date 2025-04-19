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
            self.the_start = start.replace(second=0).replace(microsecond=0).astimezone()
        self.the_end = None
        if (end is not None):
            self.the_end = end.replace(second=0).replace(microsecond=0).astimezone()
        if (start is not None and end is not None):
            if (end < start):
                self.the_end = self.the_start
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
    
    def end(self) -> datetime.datetime:
        return self.the_end

    @classmethod
    def datetime_as_iso(cls, date:datetime.datetime) -> str:
        local_date = date.astimezone()
        local_tz = local_date.tzinfo
        utc_offset = local_tz.utcoffset(local_date)
        utc_offset_hours = int(utc_offset.seconds / 60 / 60)
        utc_offset_minutes = int(((utc_offset_hours * 60 * 60) - utc_offset.seconds) * 60)
        return f"{date.isoformat(timespec='seconds')}+{utc_offset_hours:02d}:{utc_offset_minutes:02d}"

    def start_as_iso(self) -> str:
        return self.start().isoformat(timespec='seconds')
    
    def end_as_iso(self) -> str:
        return self.end().isoformat(timespec='seconds')

    def duration(self) -> datetime.timedelta:
        duration = datetime.timedelta()
        if (self.the_start is not None and self.the_end is not None):
            duration = self.the_end - self.the_start
        return duration
    
    def same_name_and_date_without_time(self, another) -> bool:
        return (
            self.name() == another.name() and
            self.start().date() == another.start().date()
        )
    
    def get_timezone_info(self):
        # TODO:
        # For now it is returning a localized string with a full name of a time zone.
        # What we do want instead, is a format like 'Europe/Warsaw',
        # and not a 'Środkowoeuropejski czas letni' 
        # (which is a full wording description uf a CET time zone)
        local_date = self.start().astimezone()
        local_tz = local_date.tzinfo
        local_tzname = local_tz.tzname(local_date)
        print(local_tzname)
    
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

    def trim_dates(self, days_count:int):
        if (days_count > 0):
            today = datetime.datetime.now().astimezone()
            last_date = today + datetime.timedelta(days=days_count)
            new_list = EventsList()
            for event in self:
                if (event.start() >= today and event.start() <= last_date):
                    new_list.add_event(event)
            return new_list
        else:
            return self
        
    def prepare_updates_lists(self, new_events_list, update_hour:bool=True):
        # This is comparing a list of new events with a current list.
        # Returns two lists: events to remove from a calendar and events to add to it.
        # If update_hour is true, if there's an event of the same name and date,
        # but with a different start hour, remove the old one and add the new one.
        list_to_remove = EventsList()
        list_to_add = EventsList()

        for new_event in new_events_list:
            if (new_event not in self):
                if (update_hour):
                    for existing_event in self:
                        # check if it's an updated hour of an existing event
                        if (existing_event.same_name_and_date_without_time(new_event)):
                            list_to_remove.add_event(existing_event)
                list_to_add.add_event(new_event)

        return (list_to_remove, list_to_add)

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

    def __add__(self, other):
        new_list = EventsList()
        for event in self:
            new_list.add_event(event)
        for event in other:
            new_list.add_event(event)
        return new_list
    
    def __iadd__(self, other):
        for event in other:
            self.add_event(event)
        return self
        
