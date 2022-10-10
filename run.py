from db import *
import fastapi
import datetime
from utils_func import log, create_minut, log_all_information

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


@api.get('/check_connect/{value}')
def check_connect(value):
    code_from_client = 'не задан'
    try:
        decrypted_key = fer_key.decrypt(value)
        code_from_client = decrypted_key.decode('utf-8')
        code_from_client = code_from_client[:-16]
    except Exception as er:
        log_all_information(f'ошибка декодирования строки при ежечасной проверке лицензии - {er}')
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_from_client in i:
            time = datetime.datetime.now().strftime('%H:%M')
            all_minut_now = create_minut(time)
            last_chec_from_bd = session.query(LicenseCodes.last_time_check).filter_by(codes=code_from_client).first()[0]
            if last_chec_from_bd is not None:
                all_minut_from_bd = create_minut(last_chec_from_bd)
                if (all_minut_now - all_minut_from_bd) < 58:
                    print(f'лицензия с кодом {code_from_client} используется два раза')
                    log(code_from_client, last_chec_from_bd, time)

            session.query(LicenseCodes).filter_by(codes=code_from_client).update({'status': 'in work'})
            session.query(LicenseCodes).filter_by(codes=code_from_client).update({'last_time_check': time})
            session.commit()
        else:
            # если кода нет в базе писать в лог
            log(code_from_client)
    return {'dont_sniff_my_requests': 'не надо снифить запросы'}


@api.get('/id_machine/{value}')
def check(value):
    decrypted_key = fer_key.decrypt(value)
    code_from_client = decrypted_key.decode('utf-8')
    code_from_client = code_from_client[:-16]
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_from_client in i:
            date_today = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
            encrypted_key = response.encrypt(bytes(date_today+code_from_client, encoding='utf-8'))
            resp = encrypted_key.decode('utf-8')

            return {'id_machine': resp}
    return {'id_machine': 'wrong'}

