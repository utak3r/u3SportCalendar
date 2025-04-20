__version__ = "0.2.0"

import datetime
from u3SportCalendar.AppConfig import AppConfig
from u3SportCalendar.GoogleCalendar import GoogleCalendar
from u3SportCalendar.Events import Event, EventsList
from u3SportCalendar.TransferMarkt_scraper import TransferMarkt_scraper

def create_and_authorize_calendar() -> GoogleCalendar:
    # Authorize Google Calendar API
    calendar = GoogleCalendar()
    calendar.authorize()
    calendar.build_service()
    return calendar

def create_scraper_object(api):
    if (api == "TransferMarkt"):
        return TransferMarkt_scraper()
    return None

def get_events(config:AppConfig):
    # Create scraper and get upcoming events for each defined source
    events = EventsList()
    for source in config.get_sources():
        scraper = create_scraper_object(source.get("api"))
        scraper.get_events(source.get("endpoint"), events)
    
    return events

def process_events(config:AppConfig, events:EventsList, calendar:GoogleCalendar):
    # Trim events between today and defined days forward
    events = events.trim_dates(config.get_how_many_days())

    # Download existing events from calendar
    existing_events = calendar.get_events(
        config.get_events_calendar(), 
        datetime.datetime.now(), 
        datetime.datetime.now() + datetime.timedelta(days=config.get_how_many_days())
        )
    # Compare the two lists and check what to add and what to update
    (tobe_removed, tobe_added) = existing_events.prepare_updates_lists(events, config.get_update_hour())

    return (tobe_removed, tobe_added)

def add_events_to_calendar(tobe_added, tobe_removed, calendar:GoogleCalendar, events_calendar):
    for event in tobe_removed:
        calendar.delete_event(events_calendar, event)
    for event in tobe_added:
        calendar.insert_event(events_calendar, event)
    return

if __name__ == "__main__":
    config = AppConfig()
    config.load()
    #config.save()

    calendar = create_and_authorize_calendar()
    events = get_events(config)
    (tobe_removed, tobe_added) = process_events(config, events, calendar)
    add_events_to_calendar(tobe_added, tobe_removed, calendar, config.get_events_calendar())
