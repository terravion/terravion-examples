import json
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2Block:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api2_domain = config.api2_domain
    def get_block(self, block_id):
        q_url = self.api2_domain
        q_url += 'blocks/' + block_id
        q_url += '?&access_token=' + self.access_token
        print q_url
        r = requests.get(q_url)
        if r.status_code == 200:
            result = r.json()
            if result:
                return result
            else:
                return None
        else:
            return None