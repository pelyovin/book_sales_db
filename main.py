import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables

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

session.close()