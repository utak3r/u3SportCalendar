import requests
from bs4 import BeautifulSoup
import datetime
from u3SportCalendar.Events import Event, EventsList
import json

class BetsAPIScraper:
    def __init__(self):
        self.base_url = "https://betsapi.com"
    
    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5756.197 Safari/537.36'}
        events = []

        soup = None
        proceed = False
        if (0):
            response = requests.get(url, headers=headers)
            if (response.status_code == 200):
                if (0):
                    with open("betsapi_debug.html", "w", encoding="utf-8") as debug_html_file:
                        debug_html_file.write(response.text)
                        debug_html_file.close()
                soup = BeautifulSoup(response.text, 'html.parser')
        else:
            html = None
            with open("betsapi_debug.html", "r", encoding="utf-8") as debug_html_file:
                html = debug_html_file.read()
                debug_html_file.close()
            soup = BeautifulSoup(html, 'html.parser')
            proceed = True

        if (proceed):
            rows = soup.find('table', class_='table table-sm').find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                league = ""
                date = None
                date_iso = None
                teams = ""
                for cell in cells:
                    cell_class = ""
                    if (cell.has_attr('class')):
                        cell_class = cell.get('class')[0]
                    if (cell_class == "league_n"):
                        league = cell.get_text()
                    if (cell_class == "dt_n"):
                        if (cell.has_attr('data-dt')):
                            date_iso = cell.get('data-dt')
                        else:
                            date = cell.get_text()
                teams = cells[3].get_text()
                events.append((league, date, date_iso, teams))
        return events


    def get_events(self, endpoint: str, events_list: EventsList):
        if (0):
            events = self.get_events_scrape(endpoint)
            for event in events:
                teams = event[3]
                teams = self.process_teams_string(teams)
                date_start = self.process_dates(event[1], event[2])
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


    def process_teams_string(self, teams) -> str:
            teams_str = teams.replace('\n', '')
            teams_str = teams_str.strip()
            teams_split = teams_str.split("   v   ")
            teams_str = teams_split[0].strip() + " - " + teams_split[1].strip()
            return teams_str

    def process_date_string(self, date) -> datetime.datetime:
        datetime_split = date.split(" ")
        date_split = datetime_split[0].split("/")
        time_split = datetime_split[1].split(":")
        year = datetime.datetime.now().year
        dateret = datetime.datetime(year, int(date_split[0]), int(date_split[1]), int(time_split[0]), int(time_split[1]))
        return dateret
    
    def process_date_iso(self, date) -> datetime.datetime:
        local_tz = datetime.datetime.now().astimezone().tzinfo
        original_date = datetime.datetime.fromisoformat(date)
        local_date = original_date.astimezone(local_tz)
        return local_date

    def process_dates(self, date_str, date_iso) -> datetime.datetime:
        date_ret = None
        if (date_iso is not None):
            date_ret = self.process_date_iso(date_iso)
        else:
            date_ret = self.process_date_string(date_str)
        return date_ret
    