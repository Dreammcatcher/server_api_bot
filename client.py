from config import api_url
import requests


req = requests.get(f'{api_url}/check/password')
#req = requests.get(f'{api_url}/che')
print(req.json())
