import json
import logging
import requests

from util import config


class TerrAvionAPI2User:
    def __init__(self, access_token):
        self.log = logging.getLogger(__name__)
        self.api2_domain = config.api2_domain
        self.access_token = access_token

    def parse_response(self, r):
        if r.status_code == 200:
            self.log.debug('-----------------Response-------------------')
            self.log.debug(json.dumps(r.json(), sort_keys=True, indent=2))
            self.log.debug('------------------------------------')
            result = r.json()
            return result
        else:
            self.log.debug('error: %s', str(r.status_code))
            self.log.debug(r.text)
            self.log.debug('-------------------------------------------------------')

    def get_user_id(self):
        q_url = self.api2_domain
        q_url += 'users/getUserId?'
        q_url += '&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)

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
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)
