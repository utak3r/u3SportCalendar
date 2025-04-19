import requests
import random
import datetime
from u3SportCalendar.Events import Event, EventsList

class Scraper:
    def __init__(self):
        self.base_url = ""
    
    def get_random_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2'
        ]
        return random.choice(user_agents)

    def get_headers(self):
        return { 'User-Agent': self.get_random_user_agent() }
    
    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        return []
    
    def get_events(self, endpoint: str, events_list: EventsList):
        if (1):
            events = self.get_events_scrape(endpoint)
            for event in events:
                teams = event[2]
                date_start = event[1]
                new_event = Event(teams, date_start, date_start + datetime.timedelta(hours=2))
                events_list.add_event(new_event)
        else:
            with open("EventsList_debug.json", "r") as events_list_file_debug:
                events_json = events_list_file_debug.read()
                events_list += EventsList.fromJson(events_json)
                events_list_file_debug.close()
        
        if (0):
            with open("EventsList_debug.json", "w") as events_list_file_debug:
                events_json = events_list.toJson()
                events_list_file_debug.write(events_json)
                events_list_file_debug.close()
