from config import api_url, license_key
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import datetime


def send_string(dates):
    key_after_encode = base64.urlsafe_b64encode(kdf.derive(b'bytes'))
    fer_key = Fernet(key_after_encode)
    encrypted_key = fer_key.encrypt(bytes(license_key + dates, encoding='utf-8'))
    e = encrypted_key.decode('utf-8')
    return e


def check_connect(url, b):
    times = datetime.datetime.now().strftime('%H:%M')
    if times[3:] == '00':
        resp = requests.get(f'{url}/check_connect/{b}')
        print(f'проверка лицензии каждый час {resp}')


def constant_check():
    a = send_string()
    while True:
        check_connect(api_url, a)


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

key_encode = base64.urlsafe_b64encode(kdf2.derive(b'string'))
respons = Fernet(key_encode)


date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
e = send_string(date)
req = requests.get(f'{api_url}/id_machine/{e}')
#req = requests.get(f'{api_url}/che')

otvet_client = req.json()['check']
decrypted_key = respons.decrypt(otvet_client)
code_from_server = decrypted_key.decode('utf-8')
datetime_today = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
print(code_from_server[:14])
if code_from_server[14:] == license_key:
    if code_from_server[:14] == datetime_today:
        print(True)
else:
    print('f')
print(req.json())
