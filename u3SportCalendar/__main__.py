__version__ = "0.1.0"

import datetime
from u3SportCalendar.AppConfig import AppConfig
from u3SportCalendar.GoogleCalendar import GoogleCalendar
from u3SportCalendar.Events import Event, EventsList
from u3SportCalendar.BetsAPI_scraper import BetsAPIScraper
from u3SportCalendar.Pogon_scraper import Pogon_scraper
from u3SportCalendar.TransferMarkt_scraper import TransferMarkt_scraper

def create_scraper_object(api):
    if (api == "BetsAPI"):
        return BetsAPIScraper()
    if (api == "Pogon"):
        return Pogon_scraper()
    if (api == "TransferMarkt"):
        return TransferMarkt_scraper()
    return None

if __name__ == "__main__":
    config = AppConfig()
    config.load()
    events_calendar = config.get_events_calendar()
    days_forward = config.get_how_many_days()
    update_hour = config.get_update_hour()
    sources = config.get_sources()
    config.save()


    # Authorize Google Calendar API
    calendar = GoogleCalendar()
    calendar.authorize()
    calendar.build_service()

    # Create scraper and get upcoming events for each defined source
    events = EventsList()
    for source in sources:
        scraper = create_scraper_object(source.get("api"))
        scraper.get_events(source.get("endpoint"), events)

    events = events.trim_dates(days_forward)
    for event in events:
        print(f"{event.get_as_text()}\n")

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
