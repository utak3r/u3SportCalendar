import requests
from bs4 import BeautifulSoup
import datetime
from u3SportCalendar.Events import Event, EventsList

class BetsAPIScraper:
    def __init__(self):
        self.base_url = "https://betsapi.com"
    
    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5756.197 Safari/537.36'}
        events = []

        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')

            rows = soup.find('table', class_='table table-sm').find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                league = ""
                date = None
                teams = ""
                for cell in cells:
                    cell_class = ""
                    if (cell.has_attr('class')):
                        cell_class = cell.get('class')[0]
                    if (cell_class == "league_n"):
                        league = cell.get_text()
                    if (cell_class == "dt_n"):
                        date = cell.get_text()
                teams = cells[3].get_text()
                events.append((league, date, teams))
        return events


    def get_events(self, endpoint: str, events_list: EventsList):
        if (0):
            events = self.get_events_scrape(endpoint)
        else:
            events = []
            events.append(('Poland Ekstraklasa', '04/19 18:15', '\n\n                                Pogon Szczecin                 v\n                Rakow Czestochowa\n\n'))
            events.append(('Poland Cup', '05/02 14:00', '\n\n                                Pogon Szczecin                 v\n                Legia Warsaw\n\n'))
            events.append(('Poland Ekstraklasa', '04/25 16:00', '\n\nPuszcza Niepolomice\n                 v\n                Pogon Szczecin                             \n'))

        for event in events:
            teams = event[2]
            teams = self.process_teams_string(teams)
            date_start = self.process_date_string(event[1])
            new_event = Event(teams, date_start, date_start + datetime.timedelta(hours=2))
            events_list.add_event(new_event)

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