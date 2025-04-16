import json

class AppConfig:
    def __init__(self):
        self.events_calendar = None

    def save(self):
        data = {
            "events_calendar": self.events_calendar
        }
        with open("config.json", "w") as jsonfile:
            json.dump(data, jsonfile)

    def load(self):
        with open("config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            self.events_calendar = data["events_calendar"]

    def get_events_calendar(self) -> str:
        return self.events_calendar

    def set_events_calendar(self, calendar):
        self.events_calendar = calendar
