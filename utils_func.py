import datetime


def log(license_code=None, first_time=None, second_time=None, stroka=None):
    with open('logs.txt', 'a', encoding='utf-8') as f:
        times = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        if second_time is not None:
            f.write(f'{times} от лицензии - {license_code} получено два ответа ({first_time}, {second_time})\n')
        elif (second_time is None) and (stroka is None):
            f.write(f'{times} поступил запрос с кодом ({license_code}) которого нет в БД\n')
        if stroka is not None:
            f.write(f'{times} запрос с кодом ({license_code}) {stroka}\n')


def log_all_information(error):
    with open('logs.txt', 'a', encoding='utf-8') as f:
        times = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        f.write(f'{times} ОШИБКА - {error}')


def create_minut(time):
    minut_hours = int(time[:1]) * 60
    minutes = int(time[3:])
    return minut_hours + minutes
