import json
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2UserBlock:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api2_domain = config.api2_domain
    def get_user_blocks_from_gps(self, user_id, lat, lng):
        q_url = self.api2_domain
        q_url += 'userBlocks/getBlocksFromGPS'
        q_url += '?userId=' + user_id
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
    def get_user_blocks_from_name(self, user_id, block_name):
        q_url = self.api2_domain
        q_url += 'userBlocks/getBlocksByName'
        q_url += '?userId=' + user_id
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
    def get_user_blocks(self, user_id):
        q_url = self.api2_domain
        q_url += 'userBlocks/getUserBlocksForMap'
        q_url += '?userId=' + user_id
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