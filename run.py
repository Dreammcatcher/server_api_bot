from db import session, LicenseCodes
import fastapi
import datetime
from utils_func import create_minut
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging

logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


api = fastapi.FastAPI(docs_url=None)
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


@api.get('/gettime/{value}')
def check_connect(value):
    code_client = 'не задан'
    time_from_client = 'не задан'
    name_bot_client = 'не задан'
    try:
        decrypted_key = fer_key.decrypt(value)
        code_from_client = decrypted_key.decode('utf-8')
        time_from_client = code_from_client[27:32]
        code_client = code_from_client[:16]
        name_bot_client = code_from_client[32:]
    except Exception as er:
        logging.warning(f'ошибка декодирования строки при ежечасной проверке лицензии - {er}')
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_client in i:
            time = datetime.datetime.now().strftime('%H:%M')
            if time_from_client != time:
                logging.warning(f'license_code-{code_client}, бот - {name_bot_client} не соответствие времени (клиент-{time_from_client}, сервер-{time}) подмена?')
            all_minut_now = create_minut(time)
            last_chec_from_bd = session.query(LicenseCodes.last_time_check).filter_by(codes=code_client).first()[0]
            if last_chec_from_bd is not None:
                all_minut_from_bd = create_minut(last_chec_from_bd)
                if (all_minut_now - all_minut_from_bd) < 58:
                    #print(f'лицензия с кодом {code_from_client} используется два раза')
                    logging.info(code_client, last_chec_from_bd, time)

            session.query(LicenseCodes).filter_by(codes=code_client).update({'status': 'in work'})
            session.query(LicenseCodes).filter_by(codes=code_client).update({'last_time_check': time})
            session.query(LicenseCodes).filter_by(codes=code_client).update({'name_bot_client': name_bot_client})
            session.commit()
            status_block = session.query(LicenseCodes.status_block).filter_by(codes=code_client).first()[0]
            if status_block is not None:
                return {'trying to change the request': '?'}

            return {'dont_sniff_my_requests': 'не надо снифить запросы'}

    # если кода нет в базе писать в лог
    logging.warning(f'code_client-{code_client}, бот-{name_bot_client} подбор кода лицензии при часовой проверке')

    return {'dont_sniff_my_requests': '!'}


@api.get('/id_machine/{value}')
def check(value):
    code_from_client = 'не задан'
    try:
        decrypted_key = fer_key.decrypt(value)
        code_from_client = decrypted_key.decode('utf-8')
        code_from_client = code_from_client[:-16]
    except Exception as er:
        date_today = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
        logging.info(f'ошибка декодирования строки при первой проверке лицензии - {er}')
        wrong_key = response.encrypt(bytes(date_today + 'wrongdecod', encoding='utf-8'))
        wrong_string = wrong_key.decode('utf-8')
        return {'id_machine': wrong_string}
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if code_from_client in i:
            date_today = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
            encrypted_key = response.encrypt(bytes(date_today+code_from_client, encoding='utf-8'))
            resp = encrypted_key.decode('utf-8')
            return {'id_machine': resp}
    date_today = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
    wrong_key = response.encrypt(bytes(date_today + 'IDDQD', encoding='utf-8'))
    wrong_string = wrong_key.decode('utf-8')
    return {'id_machine': wrong_string}


# неправильное время
@api.get('/recdata/{value}')
def wrong_time(value):
    decrypted_key = fer_key.decrypt(value)
    wrong_from_client = decrypted_key.decode('utf-8')
    logging.warning(f'ошибка - {wrong_from_client} у клиента время сервера не совпало с временем машины (часы)')


# перебор кодов лицензии при первом запуске
@api.get('/perdata/{value}')
def wrong_code(value):
    decrypted_key = fer_key.decrypt(value)
    wrong_from_client = decrypted_key.decode('utf-8')
    logging.warning(f'{wrong_from_client}, перебор кодов лицензии при первом запуске')
