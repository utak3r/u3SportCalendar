__version__ = "0.1.0"

import datetime
from u3SportCalendar.AppConfig import AppConfig
from u3SportCalendar.GoogleCalendar import GoogleCalendar
from u3SportCalendar.BetsAPI_scraper import BetsAPIScraper
from u3SportCalendar.Events import Event, EventsList

if __name__ == "__main__":
    config = AppConfig()
    config.load()
    events_calendar = config.get_events_calendar()

    use_google_calendar = False
    use_bets_scraper = True

    if (use_bets_scraper):
        scraper = BetsAPIScraper()
        events = EventsList()
        #scraper.get_events("ts/17230/Arsenal", events)
        scraper.get_events("ts/43934/Pogon-Szczecin", events)
        for event in events:
            print(f"{event.get_as_text()}\n")


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
            