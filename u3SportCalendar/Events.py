import datetime

class EventException(Exception):
    def __init__(self, msg):
        self.msg = msg
        print('EventException exception occured')


class Event:
    def __init__(self, name:str="", start:datetime=None, end:datetime=None):
        self.the_name = name
        self.the_start = start
        self.the_end = end
        if (start is not None and end is not None):
            if (end < start):
                self.the_end = start
                raise EventException("End date is sooner than start date.")
            
    def name(self) -> str:
        return self.the_name
    
    def start(self) -> datetime:
        return self.the_start
    
    def start_iso(self) -> str:
        return self.the_start.isoformat(timespec='seconds')
    
    def end(self) -> datetime:
        return self.the_end

    def end_iso(self) -> str:
        return self.the_end.isoformat(timespec='seconds')

    def duration(self) -> datetime.timedelta:
        duration = datetime.timedelta()
        if (self.the_start is not None and self.the_end is not None):
            duration = self.the_end - self.the_start
        return duration
    
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

    def __getitem__(self, key) -> Event:
        return self.the_list[key]

    def add_event(self, name, start, end):
        event = Event(name, start, end)
        self.the_list.append(event)
    