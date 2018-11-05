import json
import logging
import requests
import datetime
import traceback
import util.config as config

class TerrAvionAPI1User:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api1_domain = config.api1_domain
        self.log = logging.getLogger(__name__)
    def parse_response(self, r):
        if r.status_code == 200:
            self.log.debug('-----------------Response-------------------')
            self.log.debug(json.dumps(r.json(), sort_keys=True, indent=2))
            self.log.debug('------------------------------------')
            result = r.json()
            return result
        else:
            self.log.debug('error:' + str(r.status_code))
            self.log.debug(r.text)
            self.log.debug('-------------------------------------------------------')
    def get_user(self, user_email):
        q_url = self.api1_domain
        q_url += 'users/' + user_email
        q_url += '/?access_token=' + self.access_token
        self.log.debug(q_url)
        r = requests.get(q_url)
        return self.parse_response(r)
