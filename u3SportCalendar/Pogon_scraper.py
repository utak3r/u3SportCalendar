from u3SportCalendar.Scraper import Scraper
import requests
from bs4 import BeautifulSoup
import datetime

class Pogon_scraper(Scraper):
    def __init__(self):
        self.base_url = "https://pogonszczecin.pl"
    
    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        events = []

        response = requests.get(url, headers=self.get_headers())
        if (response.status_code == 200):
            if (0):
                with open("debug.html", "w", encoding="utf-8") as debug_html_file:
                    debug_html_file.write(response.text)
                    debug_html_file.close()
            soup = BeautifulSoup(response.text, 'html.parser')

            mecze = soup.find('div', class_='timetable-scroll-area').find_all('div', class_='timetable')
            last_month = 0
            last_year = datetime.datetime.now().year
            for mecz in mecze:
                div_result = mecz.find('div', class_='result-wrapper')
                if ('vs' in div_result.attrs.get('class')):
                    date_short = mecz.find('div', class_='date short').find('span').contents[0].strip()
                    date_date = date_short.split(', ')[0]
                    date_time = date_short.split(', ')[1]
                    month = int(date_date.split('.')[0])
                    day = int(date_date.split('.')[1])
                    hour = int(date_time.split(':')[0])
                    minute = int(date_time.split(':')[1])
                    if (month < last_month):
                        year = datetime.datetime.now().year + 1
                        last_year = year
                    else:
                        year = datetime.datetime.now().year
                    last_month = month
                    if (year < last_year):
                        year = last_year
                    date_datetime = datetime.datetime(
                        year, month, day, 
                        hour, minute
                        ).astimezone()
                    print(date_datetime)
                    team_home = mecz.find('div', class_='team team-name team-home').contents[1].contents[0].strip()
                    print(team_home)
                    team_away = mecz.find('div', class_='team team-name team-away').contents[1].contents[0].strip()
                    print(team_away)

                    events.append(('Ekstraklasa', date_datetime, f"{team_home} - {team_away}"))

        return events

