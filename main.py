import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import json

driver = 'postgresql'
login = 'postgres'
password = 'postgres'
server = 'localhost:5432'
db_name = 'book_sales'

DSN = f'{driver}://{login}:{password}@{server}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('test_data.json') as f:
    data = json.load(f)

for row in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale,
    }[row.get('model')]
    session.add(model(id=row.get('pk'), **row.get('fields')))
session.commit()


def get_book_shopping_list():
    """Функция запрашивает имя или id издателя и выводит построчно факты покупки книг этого издателя"""
    publisher_info = input('Введите id издателя или его имя: ')

    publishers_ids = [str(*i) for i in session.query(Publisher.id).all()]
    publishers_names = [str(*i) for i in session.query(Publisher.name).all()]

    def generate_filtering_request():
        """Функция формирует запрос на фильтрацию по Publisher.id или Publisher.name"""
        return Publisher.id == int(publisher_info) if publisher_info.isdigit() else Publisher.name == publisher_info

    if publisher_info in publishers_ids or publisher_info in publishers_names:
        res = session.query(Stock, Sale, Book, Shop, Publisher).\
            join(Sale.stock).\
            join(Stock.book).\
            join(Stock.shop).\
            join(Book.publisher).filter(generate_filtering_request())
        for stock, sale, book, shop, publisher in res.all():
            print(book.title.ljust(40), shop.name.ljust(15), str(sale.price).ljust(6), sale.date_sale, sep='| ')
    else:
        print('Такого издателя нет.')


if __name__ == "__main__":
    get_book_shopping_list()

session.close()
