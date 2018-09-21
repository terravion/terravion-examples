import json
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2UserBlock:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.api2_domain = config.api2_domain
    def get_user_blocks_from_gps(self, lat, lng):
        q_url = self.api2_domain
        q_url += 'userBlocks/getBlocksFromGPS'
        q_url += '?userId=' + self.user_id
        q_url += '&lat=' + lat
        q_url += '&lng=' + lng
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
    def get_user_blocks_from_name(self, block_name):
        q_url = self.api2_domain
        q_url += 'userBlocks/getBlocksByName'
        q_url += '?userId=' + self.user_id
        q_url += '&blockName=' + block_name
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
    def get_user_blocks(self):
        q_url = self.api2_domain
        q_url += 'userBlocks/getUserBlocksForMap'
        q_url += '?userId=' + self.user_id
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