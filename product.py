import json


class Product:
    def __init__(self, read_id=None):
        self.id = read_id
        self.shop_name = None
        self.name, self.url = 'name missing', 'url missing'
        self.path = []
        self.status = None
        self.price = 0
        self.features = {}
        self.rating = None
        self.quantity = None
        self.votes = {'5*': 0, '4*': 0, '3*': 0, '2*': 0, '1*': 0}
        self.order = 0

    def no_url(self):
        self.__init__(self.id)

    def out_items(self):
        return [int(self.id), self.name, self.url, *self.path, int(self.price), str(self.features)]

    def product_reviews_dict(self):
        return {'Артикул МП': int(self.id), 'Статус': self.status,
                'Наименование': self.name, 'Рейтинг': self.rating,
                'Количество отзывов на товар': self.quantity,
                '5*': self.votes['5*'], '4*': self.votes['4*'],
                '3*': self.votes['3*'], '2*': self.votes['2*'],
                '1*': self.votes['2*'],
                # 'scores': self.votes,
                'Категория': self.path,
                'url': self.url}

    def json_items(self):
        return {self.id: [self.name, self.url, *self.path, self.price, self.features]}

    def json_items_write(self):
        with open('json_result_data.json', "a") as file:
            json.dump(self.json_items(), file, ensure_ascii=False)
            file.write('\n')
