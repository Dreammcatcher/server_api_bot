import configparser
import datetime
import string
import random
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from cryptography.fernet import Fernet
from sqlalchemy.orm import sessionmaker
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

conf = configparser.ConfigParser()

Base = declarative_base()


class LicenseCodes(Base):
    __tablename__ = 'db_liscense_codes_v1.2'
    id = Column(Integer, primary_key=True)
    codes = Column('codes', String, default=None)
    date_sell = Column('date_sell', Date, default=None, onupdate=datetime.date.today())
    status = Column('status', String, default=None)
    last_time_check = Column('last_time_check', String, default=None)

    def __str__(self):
        pass


engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_codes(quantity_codes: int):
    """
    заполняет БД кодами
    :param quantity_codes: количество создаваемых кодов
    """
    letters = string.ascii_uppercase + string.digits
    for i in range(1, quantity_codes):
        code = ''.join(random.choice(letters) for j in range(16))
        one = LicenseCodes(codes=code)
        session.add(one)
    session.commit()


create_codes(101)
