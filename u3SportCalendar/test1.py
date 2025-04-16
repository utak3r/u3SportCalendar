import datetime
from AppConfig import AppConfig
from GoogleCalendar import GoogleCalendar


def main():
  
    config = AppConfig()
    config.load()
    events_calendar = config.get_events_calendar()

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
        return



if __name__ == "__main__":
    main()
