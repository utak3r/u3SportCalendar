__version__ = "0.1.0"

import datetime
from u3SportCalendar.AppConfig import AppConfig
from u3SportCalendar.GoogleCalendar import GoogleCalendar

if __name__ == "__main__":
    config = AppConfig()
    config.load()
    events_calendar = config.get_events_calendar()

    use_google_calendar = False

    if (use_google_calendar):
        calendar = GoogleCalendar()
        calendar.authorize()
        calendar.build_service()

        start = datetime.datetime.now(tz=datetime.timezone.utc)
        end = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=7)

        events = calendar.get_events(events_calendar, start, end)
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

        if not events:
            print("No upcoming events found.")
            