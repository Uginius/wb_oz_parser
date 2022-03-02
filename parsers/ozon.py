import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from config import wait_time
from parsers.parsers import Parser


class ParserOz(Parser):

    def search_id_to_url(self):
        try:
            self.browser.get(url=self.product.url)
            # print(f'{self.product.id}: connecting to search url {self.product.url}')
            time.sleep(3)
            data = BeautifulSoup(self.browser.page_source, 'lxml').find('div', attrs={"data-widget": "searchResultsV2"})
            self.product.url = 'https://www.ozon.ru' + data.find('a')['href'].split('/?asb')[0]
        except Exception as ex:
            print('Search error:', ex)
            self.product.url = None

    def get_page_from_url(self):
        self.search_id_to_url()
        if not self.product.url:
            return
        self.connection_info()
        self.browser.get(url=self.product.url)
        self.page_scroll()
        time.sleep(wait_time)
        self.page_data = BeautifulSoup(self.browser.page_source, 'lxml')
        # self.write_html()

    def page_scroll(self):
        # while True:
        #     self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     try:
        #         time.sleep(1)
        #         self.browser.find_element(By.ID, "comments")
        #     except Exception as e:
        #         print(e)
        #         continue  # Не нашли элемент, попробуем на следующей итерации
        self.browser.execute_script("window.scrollBy(0, 1000)")
        time.sleep(1)
        self.browser.execute_script("window.scrollBy(0, 1000)")
        time.sleep(1)
        self.browser.execute_script("window.scrollBy(0,-1000)")

    def parse_page(self):
        self.product.name = ' '.join(self.page_data.find('h1').text.strip().split())
        reviews_block = self.page_data.find('div', attrs={"data-widget": "webReviewProductScore"}).a['title']
        self.product.quantity = int(reviews_block.split()[0])
        self.get_votes()

    def get_votes(self):
        votes_stars_parent = self.page_data.find(text='5 звезд').parent.parent
        self.product.rating = float(votes_stars_parent.parent.parent.find('span').text.split()[0])
        votes_class = votes_stars_parent.find_all('div')[4]['class'][0]
        votes = [vote.text for vote in self.page_data.find_all('div', class_=votes_class)]
        self.product.votes = dict(zip(['5*', '4*', '3*', '2*', '1*'], votes))
