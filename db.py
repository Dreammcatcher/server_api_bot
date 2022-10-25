import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class LicenseCodes(Base):
    __tablename__ = 'db_liscense_codes_v1.5'
    id = Column(Integer, primary_key=True)
    codes = Column('codes', String, default=None)
    date_sell = Column('date_sell', Date, default=None, onupdate=datetime.date.today())
    status = Column('status', String, default=None)
    last_time_check = Column('last_time_check', String, default=None)
    name_bot_client = Column('name_bot_client', String, default=None)
    status_block = Column('status_block', String, default=None)


engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# def create_codes(quantity_codes: int):
#     """
#     заполняет БД кодами
#     :param quantity_codes: количество создаваемых кодов
#     """
#     letters = string.ascii_uppercase + string.digits
#     for i in range(1, quantity_codes):
#         code = ''.join(random.choice(letters) for j in range(16))
#         one = LicenseCodes(codes=code)
#         session.add(one)
#     session.commit()
#
#
# create_codes(101)
