import time
from bs4 import BeautifulSoup
from config import wait_time
from parsers.parsers import Parser


class ParserWb(Parser):

    def get_page_from_url(self):
        self.connection_info()
        self.browser.get(url=self.product.url)
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0, window.scrollY - 200)")
        time.sleep(wait_time)
        self.page_data = BeautifulSoup(self.browser.page_source, 'lxml')

    def parse_page(self):
        self.product.name = self.page_data.find('h1').text
        self.product.quantity = self.page_data.find('span', class_='same-part-kt__count-review').text.strip().split()[0]
        if self.product.quantity == '0':
            return
        self.get_rating()

    def get_rating(self):
        try:
            html_rating = self.page_data.find('div', class_='user-scores__rating')
            votes = [vote.text for vote in html_rating.find_all('span', class_='progress-lines__percent')]
            self.product.votes = dict(zip(['5*', '4*', '3*', '2*', '1*'], votes))
            self.product.rating = float(html_rating.find('span', class_='user-scores__score').text)
            for key, value in self.product.votes.items():
                votes = int(round((int(value[:-1]) * int(self.product.quantity)) / 100, 0))
                self.product.votes[key] = votes
        except Exception as ex:
            print(f'{self.product.id}: rating error - {ex}')
