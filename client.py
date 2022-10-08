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
date = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
key_after_encode = base64.urlsafe_b64encode(kdf.derive(b'bytes'))
fer_key = Fernet(key_after_encode)
encrypted_key = fer_key.encrypt(bytes(license_key+date, encoding='utf-8'))
e = encrypted_key.decode('utf-8')
req = requests.get(f'{api_url}/check/{e}')
#req = requests.get(f'{api_url}/che')
print(req.json())
