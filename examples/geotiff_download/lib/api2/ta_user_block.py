import json
import logging
import requests

from util import config


class TerrAvionAPI2UserBlock:
    def __init__(self, user_id, access_token):
        self.log = logging.getLogger(__name__)
        self.api2_domain = config.api2_domain

        self.user_id = user_id
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

    def get_user_blocks_from_gps(self, lat, lng):
        q_url = self.api2_domain
        q_url += 'userBlocks/getBlocksFromGPS'
        q_url += '?userId=' + self.user_id
        q_url += '&lat=' + lat
        q_url += '&lng=' + lng
        q_url += '&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)

    def get_user_blocks_from_name(self, block_name):
        q_url = self.api2_domain
        q_url += 'userBlocks/getBlocksByName'
        q_url += '?userId=' + self.user_id
        q_url += '&blockName=' + block_name
        q_url += '&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)

    def get_user_blocks(self):
        q_url = self.api2_domain
        q_url += 'userBlocks/getUserBlocksForMap'
        q_url += '?userId=' + self.user_id
        q_url += '&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)
