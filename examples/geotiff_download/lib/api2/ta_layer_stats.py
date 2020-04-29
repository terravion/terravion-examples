import json
import logging
import requests

from util import config


class TerrAvionAPI2LayerStats:
    def __init__(self, user_id, access_token):
        self.log = logging.getLogger(__name__)
        self.api2_domain = config.api2_domain
        self.access_token = access_token
        self.user_id = user_id

    def get_layer_thresholds(self, layer_id, product=None):
        # TODO: pagination
        q_url = self.api2_domain
        q_url += 'layerStats/getColormapThresholds/'
        q_url += '?access_token=' + self.access_token
        q_url += '&userId=' + self.user_id

        if layer_id:
            q_url += '&layerId=' + layer_id

        if product:
            q_url += '&product=' + product

        logging.debug('q_url: %s', q_url)

        r = requests.get(q_url)
        logging.debug('status code: %s', str(r.status_code))

        if r.status_code == 200:
            result = r.json()
            if result:
                return result
            else:
                return None
        else:
            return None

    def get_layer_stats_by_layer_id(self, layer_id):
        q_url = self.api2_domain
        q_url += 'layerStats/getLayerStatsByLayerId/'
        q_url += '?access_token=' + self.access_token
        # q_url += '&userId=' + self.user_id
        q_url += '&layerId=' + layer_id

        logging.debug('q_url: %s', q_url)

        r = requests.get(q_url)
        logging.debug('status code: %s', str(r.status_code))

        if r.status_code == 200:
            result = r.json()
            if result:
                return result[0]
            else:
                return None
        else:
            return None
