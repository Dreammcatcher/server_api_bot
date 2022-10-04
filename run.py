
import fastapi


api = fastapi.FastAPI()


@api.get('/check')
def check():
    return {'check': 'True'}


@api.get('/check/{value}')
def check(value):
    if value == 'password':
        return {'check': 'it is password'}
    else:
        return {'check': 'WARNING'}

