import requests
import random
from bs4 import BeautifulSoup
import datetime
from u3SportCalendar.Scraper import Scraper
from u3SportCalendar.Events import Event, EventsList
import json

class BetsAPIScraper(Scraper):
    def __init__(self):
        self.base_url = "https://betsapi.com"

    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        events = []

        response = requests.get(url, headers=self.get_headers())
        if (response.status_code == 200):
            if (1):
                with open("debug.html", "w", encoding="utf-8") as debug_html_file:
                    debug_html_file.write(response.text)
                    debug_html_file.close()
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
                        if (cell.has_attr('data-dt')):
                            date = self.process_date(cell.get('data-dt'))
                teams = self.process_teams_string(cells[3].get_text())
                events.append((league, date, teams))

        return events

    def process_teams_string(self, teams) -> str:
            teams_str = teams.replace('\n', '')
            teams_str = teams_str.strip()
            teams_split = teams_str.split("   v   ")
            teams_str = teams_split[0].strip() + " - " + teams_split[1].strip()
            return teams_str

    def process_date(self, date) -> datetime.datetime:
        local_tz = datetime.datetime.now().astimezone().tzinfo
        original_date = datetime.datetime.fromisoformat(date)
        local_date = original_date.astimezone(local_tz)
        return local_date
