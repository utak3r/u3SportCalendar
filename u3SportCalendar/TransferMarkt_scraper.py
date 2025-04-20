from u3SportCalendar.Scraper import Scraper
import requests
from bs4 import BeautifulSoup
import datetime

class TransferMarkt_scraper(Scraper):
    def __init__(self):
        self.base_url = "https://www.transfermarkt.com/"

    def get_events_scrape(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        events = []

        response = requests.get(url, headers=self.get_headers())
        if (response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')
            responsive_table_div = soup.find('div', class_='responsive-table')
            responsive_table = responsive_table_div.find('table')
            responsive_table_tbody = responsive_table.find('tbody')
            mecze = responsive_table_tbody.findAll('tr')
            for mecz in mecze:
                if (len(mecz.contents) > 5):
                    print(mecz)
