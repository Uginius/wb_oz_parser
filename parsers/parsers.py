import time

from bs4 import BeautifulSoup

from config import wait_time


class Parser:

    def __init__(self, product, browser):
        self.product = product
        self.browser = browser
        self.page_data = None

    def run(self):
        try:
            self.get_page_from_url()
            self.parse_page()
        except Exception as ex:
            print('ERROR', ex)

    def get_page_from_url(self):
        self.browser.get(url=self.product.url)
        time.sleep(wait_time)
        self.page_data = BeautifulSoup(self.browser.page_source, 'lxml')

    def connection_info(self):
        print(f'{self.product.order:3} - {self.product.shop_name}/{self.product.id} Соединяемся с {self.product.url}')

    def parse_page(self):
        pass

    def data_to_out(self):
        return {'Ссылка на товар (url)': self.product.url,
                'Полное наименование': self.product.name,
                'ID товара': self.product.id,
                'product_scores': self.product.votes,
                'Рейтинг': self.product.rating,
                'Количество': self.product.quantity}

    def write_html(self):
        with open(f'htmls/{self.product.shop_name}_{self.product.id}.html', "w") as write_file:
            write_file.write(self.browser.page_source)

    def read_html(self, filename=None):
        if not filename:
            filename = f'htmls/{self.product.shop_name}_{self.product.id}.html'
        with open(filename, "r", encoding='utf8') as read_file:
            self.page_data = BeautifulSoup(read_file.read(), 'lxml')
