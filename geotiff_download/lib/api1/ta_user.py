import json
import requests
import datetime
import traceback
import util.config as config

class TerrAvionAPI1User:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api1_domain = config.api1_domain
    def get_user(self, user_email):
        q_url = self.api1_domain
        q_url += 'users/' + user_email
        q_url += '/?access_token=' + self.access_token
        print(q_url)
        r = requests.get(q_url)
        print('status code', r.status_code)
        if r.status_code == 200:
            result = r.json()
            if result:
                return result
            else:
                return None
        else:
            return None