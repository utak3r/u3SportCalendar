from u3SportCalendar.Scraper import Scraper
import requests
from bs4 import BeautifulSoup
import datetime
import time

class TransferMarkt_scraper(Scraper):
    def __init__(self):
        self.base_url = "https://www.transfermarkt.com/"

    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        events = []

        response = requests.get(url, headers=self.get_headers())
        if (response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the team name
            headline = soup.find('div', class_='data-header__headline-container')
            team_name = headline.find('h1').text.strip()

            # Find the matches
            responsive_table_div = soup.find('div', class_='responsive-table')
            responsive_table = responsive_table_div.find('table')
            responsive_table_tbody = responsive_table.find('tbody')
            mecze = responsive_table_tbody.findAll('tr')
            league = ""
            for mecz in mecze:
                if (len(mecz.contents) > 5):
                    tds = mecz.findAll('td')
                    # check if it's a fixture or already played match
                    match_report_or_preview = tds[9].contents[0].attrs.get('title')
                    if (match_report_or_preview == 'Match preview'):
                        date_datetime = self.process_datetime(tds[1].text.strip(), tds[2].text.strip())
                        home_or_away = tds[3].text.strip()
                        opponent = tds[6].find('a').text.strip()
                        if (home_or_away == 'H'):
                            teams_match = f"{team_name} - {opponent}"
                        else:
                            teams_match = f"{opponent} - {team_name}"
                        
                        events.append((league, date_datetime, teams_match))
                        print(f"{league}: {teams_match}, {date_datetime}")
                else:
                    league = mecz.find('td').find('img').attrs.get('title')
        return events

    def process_datetime(self, date_str, time_str) -> datetime.datetime:
        # TODO:
        # It looks like it's interpreting 12:00 AM as midnight (00:00), instead od a noon...
        date_split = date_str.split(' ')[1].split('/')
        date_year = int(date_split[2]) + 2000
        date_month = int(date_split[0])
        date_day = int(date_split[1])
        time_part = time.strptime(time_str, '%I:%M %p')
        date_datetime = datetime.datetime(date_year, date_month, date_day, time_part.tm_hour, time_part.tm_min)
        return date_datetime
