import csv
import datetime
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import browser_path
from parsers.ozon import ParserOz
from parsers.wb import ParserWb
from product import Product


class Platform(Thread):
    def __init__(self, platform_name):
        super().__init__()
        self.platform = platform_name
        self.goods = []
        self.parser = None
        self.browser = None
        self.platform_order = 0
        self.data_from_page = None
        self.product_titles = ['ID товара',
                               'Полное наименование',
                               'Рейтинг',
                               'Цель из Ф4',
                               'Необходимое кол-во отзывов с 5*',
                               'Количество',
                               '5*', '4*', '3*', '2*', '1*',
                               'Ссылка на товар (url)',
                               ]
        self.write_data = self.product_titles
        self.result_file = f'results/{self.platform}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}'

    def run(self):
        self.get_id_from_file()
        self.start_parsing()
        # self.data_out()

    def get_id_from_file(self):
        id_filename, url, second = '', '', ''
        match self.platform:
            case 'oz':
                id_filename = 'id_for_use/id_oz.txt'
                url = 'https://www.ozon.ru/search/?from_global=true&text='
                self.parser = ParserOz
            case 'wb':
                id_filename = 'id_for_use/id_wb.txt'
                url = 'https://www.wildberries.ru/catalog/'
                second = '/detail.aspx?targetUrl=EX#Comments'
                self.parser = ParserWb
            case _:
                print('ERROR loading id_file')
        with open(id_filename, "r") as read_file:
            for line in read_file:
                try:
                    product = Product(int(line))
                    product.url = url + str(product.id) + second
                    product.shop_name = self.platform
                    self.platform_order += 1
                    product.order = self.platform_order
                    self.goods.append(product)
                except Exception as ex:
                    print(self.platform, ex)

    def data_out(self):
        for product in self.goods:
            print(f'platform: {self.platform} -- №{product.order} -- id: {product.id} -- url: {product.url}')

    def start_parsing(self):
        write_data = self.write_data_to_csv
        # write_data = self.write_data_to_text
        write_data()
        browser = webdriver.Chrome(service=Service(executable_path=browser_path))
        for product in self.goods:
            current_parser = self.parser(product, browser)
            current_parser.run()
            self.data_from_page = current_parser.data_to_out()
            self.collect_data_to_write()
            write_data()
        if browser:
            browser.close()

    def collect_data_to_write(self):
        collect_line = self.data_from_page | self.data_from_page['product_scores']
        collect_line['Цель из Ф4'] = 4
        if not self.data_from_page['Рейтинг']:
            collect_line['Необходимое кол-во отзывов с 5*'] = 'Работа с отзывами'
        elif self.data_from_page['Рейтинг'] < collect_line['Цель из Ф4']:
            mark = [0, int(collect_line['1*']), int(collect_line['2*']),
                    int(collect_line['3*']), int(collect_line['4*']), int(collect_line['5*'])]
            result = mark[4] + mark[3] * 3 + mark[2] * 5 + mark[1] * 7 - mark[5]
            collect_line['Необходимое кол-во отзывов с 5*'] = f'Нужно еще {result} отзывов на 5*'
        else:
            collect_line['Необходимое кол-во отзывов с 5*'] = 'Все ОК'
        self.write_data = [collect_line[key] for key in self.product_titles]

    def write_data_to_csv(self):
        filename = self.result_file + '.csv'
        with open(filename, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.write_data)

    def write_data_to_text(self):
        to_write = [str(el) for el in self.write_data]
        filename = self.result_file + '.txt'
        with open(filename, "a", newline='') as write_file:
            write_file.write(';'.join(to_write) + '\n')
