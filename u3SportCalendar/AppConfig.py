import json

class AppConfig:
    def __init__(self):
        self.config_file_name = "config.json"
        self.default_events_calendar = "primary"
        self.events_calendar = self.default_events_calendar
        self.default_how_many_days = 14
        self.how_many_days = self.default_how_many_days
        self.default_update_hour = True
        self.update_hour = self.default_update_hour

    def save(self):
        data = {
            "events_calendar": self.events_calendar,
            "how_many_days": self.how_many_days,
            "update_hour": self.update_hour
        }
        with open(self.config_file_name, "w") as jsonfile:
            json.dump(data, jsonfile)
            jsonfile.close()

    def load(self):
        with open(self.config_file_name, "r") as jsonfile:
            data = json.load(jsonfile)
            if ("events_calendar" in data):
                self.events_calendar = data["events_calendar"]
            if ("how_many_days" in data):
                self.how_many_days = data["how_many_days"]
            if ("update_hour" in data):
                self.update_hour = data["update_hour"]
            jsonfile.close()

    def get_events_calendar(self) -> str:
        if (self.events_calendar is None or self.events_calendar == ""):
            return self.default_events_calendar
        else:
            return self.events_calendar

    def set_events_calendar(self, calendar:str):
        if (calendar is not None and calendar != ""):
            self.events_calendar = calendar

    def get_how_many_days(self) -> int:
        if (self.how_many_days is not None and self.how_many_days > 0):
            return self.how_many_days
        else:
            return self.default_how_many_days
    
    def set_how_many_days(self, days:int):
        if (days is not None and days > 0):
            self.how_many_days = days

    def get_update_hour(self) -> bool:
        return self.update_hour

    def set_update_hour(self, update:bool):
        self.update_hour = update

    