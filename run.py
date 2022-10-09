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


def create_minut(time):
    minut_hours = int(time[:1]) * 60
    minutes = int(time[1:])
    return minut_hours + minutes


@api.get('/check_connect/{value}')
def check_connect(value):
    decrypted_key = fer_key.decrypt(value)
    code_from_client = decrypted_key.decode('utf-8')
    code_from_client = code_from_client[:-16]
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_from_client in i:
            time = datetime.datetime.now().strftime('%H:%M')
            all_minut_now = create_minut(time)
            last_chec_from_bd = session.query(LicenseCodes.last_time_check).filter_by(codes=code_from_client).first()[0]
            all_minut_from_bd = create_minut(last_chec_from_bd)
            if (all_minut_now - all_minut_from_bd) < 58:

                # писать в лог что два ключа

                pass

            session.query(LicenseCodes).filter_by(codes=code_from_client).update({'status': 'in work'})
            session.query(LicenseCodes).filter_by(codes=code_from_client).update({'last_time_check': time})
            session.commit()
        else:
            # если кода нет в базе писать в лог
            pass


@api.get('/check/{value}')
def check(value):
    decrypted_key = fer_key.decrypt(value)
    code_from_client = decrypted_key.decode('utf-8')
    code_from_client = code_from_client[:-16]
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_from_client in i:
            date_today = datetime.date.today().strftime('%d/%m/%Y %H:%M')
            encrypted_key = response.encrypt(bytes(date_today+code_from_client, encoding='utf-8'))
            resp = encrypted_key.decode('utf-8')

            return {'id_machine': resp}
    return {'check': 'wrong'}

