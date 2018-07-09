import json
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2User:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api2_domain = config.api2_domain
    def get_user(self, user_email):
        q_url = self.api2_domain
        q_url += 'users/?filter='
        query_dic = {}
        query_dic['where'] = {}
        where_dic = {}
        if user_email:
            where_dic = {'email': user_email}
        else:
            return None
        query_dic['where'] = where_dic
        q_url += json.dumps(query_dic)
        q_url += '&access_token=' + self.access_token
        print q_url
        r = requests.get(q_url)
        print 'status code', r.status_code
        if r.status_code == 200:
            result = r.json()
            if result:
                return result
            else:
                return None
        else:
            return None