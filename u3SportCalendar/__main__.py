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
    days_forward = config.get_how_many_days()
    update_hour = config.get_update_hour()
    config.save()

    use_google_calendar = True
    use_bets_scraper = True

    if (use_google_calendar):
        calendar = GoogleCalendar()
        calendar.authorize()
        calendar.build_service()


    if (use_bets_scraper):
        scraper = BetsAPIScraper()
        events = EventsList()
        #scraper.get_events("ts/17230/Arsenal", events)
        scraper.get_events("ts/43934/Pogon-Szczecin", events)
        events = events.trim_dates(days_forward)
        for event in events:
            print(f"{event.get_as_text()}\n")

        if (use_google_calendar):
            # download existing events from calendar
            existing_events = calendar.get_events(
                events_calendar, 
                datetime.datetime.now(), 
                datetime.datetime.now() + datetime.timedelta(days=days_forward)
                )
            (tobe_removed, tobe_added) = existing_events.prepare_updates_lists(events, update_hour)

            for event in tobe_removed:
                calendar.delete_event(events_calendar, event)
            for event in tobe_added:
                calendar.insert_event(events_calendar, event)


"""     if (use_google_calendar):
        calendar = GoogleCalendar()
        calendar.authorize()
        calendar.build_service()

        start = datetime.datetime.now(tz=datetime.timezone.utc)
        end = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=days_forward)

        events = calendar.get_events(events_calendar, start, end)
        events_json = events.toJson()

        if (len(events) == 0):
            print("No upcoming events found.")
 """            