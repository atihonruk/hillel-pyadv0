import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urljoin

import requests
from django.db import connection


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

DEBUG = True
ROOT_URLCONF = __name__
SECRET_KEY = 'secret'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'immunization.sqlite3'
    }
}

BASE_URL = 'https://data.gov.ua/dataset/4cced549-1a03-4e0b-afbb-461febb26007/resource/b4d8df31-8ecc-4646-a373-95b756fde8ea/download/'

CREATE = {
    'immunization_vaccine_codes': 'create table if not exists immunization_vaccine_codes (vaccine_code char(20), vaccine_name text)',

}


def insert_into_db(tblname, tmp_name):
    create = CREATE[tblname]

    # создаем таблицу, если еще не создана

    with connection.cursor() as cur:
        cur.execute(create)
        print(f'create {tblname}', cur.rowcount)

    # удаляем старые записи

    with connection.cursor() as cur:
        delete = f'delete from {tblname}'
        cur.execute(delete)
        print(delete, cur.rowcount)

    # вставляем записи из файла

    with open(tmp_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        names = ','.join(header)
        values = ','.join(['%s'] * len(header))
        insert = f'insert into {tblname} ({names}) values ({values})'
        with connection.cursor() as cur:
            cur.executemany(insert, reader)
            print(insert, cur.rowcount)


def load_file(fname, tmp):
    # headers = {'If-None-Match': '"603caf07-4c7a"'}

    url = urljoin(BASE_URL, fname + '.csv')
    with requests.get(url, stream=True) as res:
        if res.status_code == requests.codes.ok:  # 200
            # пишем данные в файл по мере поступления :)
            for chunk in res.iter_content(chunk_size=8192):
                tmp.write(chunk)
        else:
            print(f'{fname}: {res.reason} {res.status_code}')


if __name__ == '__main__':
    try:
        tmp = NamedTemporaryFile(delete=False)
        load_file('immunization_vaccine_codes', tmp)
        tmp.close()
        insert_into_db('immunization_vaccine_codes', tmp.name)
    finally:
        print('TODO: delete {tblname}')
        # os.unlink()
