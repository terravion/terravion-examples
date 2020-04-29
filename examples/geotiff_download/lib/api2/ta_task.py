import json
import logging
import requests
from util import config


class TerrAvionAPI2Task:
    def __init__(self, user_id, access_token):
        self.log = logging.getLogger(__name__)
        self.api2_domain = config.api2_domain

        self.access_token = access_token
        self.user_id = user_id

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

    def request_geotiff_task(self, layer_id, multiband=None,
                             geotiff_epsg=None, colormap=None):
        if not self.user_id:
            self.log.debug('missing user_id')
            return None

        if not layer_id:
            self.log.debug('missing layer_id')
            return None

        q_url = self.api2_domain
        q_url += 'tasks/requestGeotiffTask'
        q_url += '?userId=' + self.user_id
        q_url += '&layerId=' + layer_id

        if multiband:
            q_url += '&multiband=true'

        if geotiff_epsg:
            q_url += '&epsgCode=' + geotiff_epsg

        if colormap:
            q_url += '&colorMap=' + colormap
            q_url += '&colormapRgb=false'

        q_url += '&access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.post(q_url)

        return self.parse_response(r)

    def get_task_info(self, task_id):
        if not task_id:
            self.log.debug('missing task_id')
            return None

        q_url = self.api2_domain
        q_url += 'tasks/' + task_id
        q_url += '?access_token=' + self.access_token
        self.log.debug(q_url)

        r = requests.get(q_url)

        return self.parse_response(r)
