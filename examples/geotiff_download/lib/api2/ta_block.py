import json
import logging
import requests

from util import config


class TerrAvionAPI2Block:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api2_domain = config.api2_domain
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

    def get_block(self, block_id):
        self.log.debug('get_block')

        q_url = self.api2_domain
        q_url += 'blocks/' + block_id
        q_url += '?&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)

    def get_geom(self, block_id):
        self.log.debug('get_geom')

        q_url = self.api2_domain
        q_url += 'blocks/' + block_id
        q_url += '/geom.geojson?&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)
