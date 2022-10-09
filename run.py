from db import *
import fastapi
import datetime

api = fastapi.FastAPI()
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'bytesstring',
    iterations=390000,)

key_after_encode = base64.urlsafe_b64encode(kdf.derive(b'bytes'))
fer_key = Fernet(key_after_encode)

kdf2 = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'string',
    iterations=390000,)

key_encode = base64.urlsafe_b64encode(kdf2.derive(b'string'))
response = Fernet(key_encode)


@api.get('/check')
def check():
    return {'check': 'True'}


@api.get('/check/{value}')
def check(value):
    decrypted_key = fer_key.decrypt(value)
    code_from_client = decrypted_key.decode('utf-8')
    code_from_client = code_from_client[:-16]
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_from_client in i:
            date_today = datetime.date.today().strftime('%d/%m/%Y')
            encrypted_key = response.encrypt(bytes(date_today+code_from_client, encoding='utf-8'))
            resp = encrypted_key.decode('utf-8')

            return {'check': resp}
    return {'check': 'wrong'}

