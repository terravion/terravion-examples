import json
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2Layer:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api2_domain = config.api2_domain
    def get_layers(self, block_id):
        q_url = self.api2_domain
        if block_id:
            q_url += 'layers/getLayersFromBlockId'
            q_url += '?blockId=' + block_id
            q_url += '&access_token=' + self.access_token
            print q_url
        else:
            return None
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


