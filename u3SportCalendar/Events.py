import datetime

class EventException(Exception):
    def __init__(self, msg):
        self.msg = msg
        print('EventException exception occured')


class Event:
    def __init__(self, name:str="", start:datetime=None, end:datetime=None):
        self.name = name
        self.dateStart = start
        self.dateEnd = end
        if (start is not None and end is not None):
            if (end < start):
                self.dateEnd = start
                raise EventException("End date is sooner than start date.")
            
    def get_duration(self) -> datetime.timedelta:
        duration = datetime.timedelta()
        if (self.dateStart is not None and self.dateEnd is not None):
            duration = self.dateEnd - self.dateStart
        return duration
    

class EventsList:
    def __init__(self):
        self.the_list = []

    def __getitem__(self, key) -> Event:
        return self.the_list[key]

    def add_event(self, name, start, end):
        event = Event(name, start, end)
        self.the_list.append(event)
    