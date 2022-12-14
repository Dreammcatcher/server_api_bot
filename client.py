import asyncio
from config import api_url, license_key
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import datetime

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'bytesstring',
    iterations=390000,)

kdf2 = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'string',
    iterations=390000,)

key_after_encode = base64.urlsafe_b64encode(kdf.derive(b'bytes'))
fer_key = Fernet(key_after_encode)


def encrypt_id_machine(dates):
    #encrypted_key = fer_key.encrypt(bytes(license_key + dates, encoding='utf-8'))
    encrypted_key = fer_key.encrypt(bytes('DDDD' + dates, encoding='utf-8'))
    t = encrypted_key.decode('utf-8')
    return t


async def check_connect(url, b):
    times = datetime.datetime.now().strftime('%H:%M')
    if times[3:] == '29':
        requests.get(f'{url}/check_connect/{b}')
        print(f'проверка лицензии каждый час')
    else:
        print('toko proveril')
    await asyncio.sleep(55)


async def constant_check():
    while True:
        dates = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        a = encrypt_id_machine(dates)
        await check_connect(api_url, a)
        await asyncio.sleep(3600)


def senc_id_machine(): # отправка лицензии для регистрации
    key_encode = base64.urlsafe_b64encode(kdf2.derive(b'string'))
    respons = Fernet(key_encode)
    date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    e = encrypt_id_machine(date)
    req = requests.get(f'{api_url}/id_machine/{e}')
    otvet_client = req.json()['id_machine']

    decrypted_key = respons.decrypt(otvet_client)
    code_from_server = decrypted_key.decode('utf-8')
    datetime_today = datetime.datetime.now().strftime('%d/%m/%Y %H')
    if code_from_server[16:] == license_key:
        if code_from_server[:13] == datetime_today:
            print('код совпадает')
            return '0b8cOf1e'
        else:
            print('дата не совпадает - отправка на сервер')
    else:
        print('ошибка, вы нарушили')
    print(req.json())

#senc_id_machine()
#if __name__ == '__main__':
#loop = asyncio.get_event_loop()
#loop.create_task(constant_check())
#asyncio.run(constant_check())
