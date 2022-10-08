from db import *
import fastapi


api = fastapi.FastAPI()


@api.get('/check')
def check():
    return {'check': 'True'}


@api.get('/check/{value}')
def check(value):
    keys_from_server = session.query(LicenseCodes.codes).all()
    for i in keys_from_server:
        if value in i:
            return {'check': 'it is password'}
    return {'check': 'WARNING'}

