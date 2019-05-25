import json
import logging
import requests
import datetime
import traceback
import util.config as config
from lib.api2.ta_user_block import TerrAvionAPI2UserBlock

class TerrAvionAPI2Layer:
    def __init__(self, user_id, access_token, epoch_start=None,
        epoch_end=None, add_epoch_start=None,
        add_epoch_end=None):
        self.api2_domain = config.api2_domain
        self.user_id = user_id
        self.access_token = access_token
        self.epoch_start = epoch_start
        self.epoch_end = epoch_end
        self.add_epoch_start = add_epoch_start
        self.add_epoch_end = add_epoch_end
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
    def get_layers_by_lat_lng(self, lat, lng):
        maser_layer_list = []
        ta2_user_block = TerrAvionAPI2UserBlock(self.user_id, self.access_token)
        user_blocks = ta2_user_block.get_user_blocks_from_gps(lat, lng)
        if user_blocks:
            for user_block in user_blocks:
                layers = self.get_layers(block_id=user_block['blockId'])
                if layers:
                    maser_layer_list += layers
        return maser_layer_list
    def get_layers_by_block_id_list(self, block_id_list):
        maser_layer_list = []
        for block_id in block_id_list:
            self.log.debug('block_id: %s', block_id)
            layers = self.get_layers(block_id=block_id)
            if layers:
                maser_layer_list += layers
        return maser_layer_list

    def get_layers(self, block_id=None, field_name=None):
        self.log.debug('get_layers')
        # TODO: pagination
        q_url = self.api2_domain
        q_url += 'users/'+ self.user_id +'/getLayers?'
        q_url += 'access_token=' + self.access_token
        if not block_id and self.epoch_start and self.epoch_end\
            and self.add_epoch_start and self.add_epoch_end and field_name:
            self.log.debug('please supply an filter')
            return None
        if block_id:
            q_url += '&blockId=' + block_id
        if field_name:
            q_url += '&fieldName=' + field_name

        if self.epoch_start:
            q_url += '&epochStart=' + str(self.epoch_start)
        if self.epoch_end:
            q_url += '&epochEnd=' + str(self.epoch_end)
        if self.add_epoch_start:
            q_url += '&addEpochStart=' + str(self.add_epoch_start)
        if self.add_epoch_end:
            q_url += '&addEpochEnd=' + str(self.add_epoch_end)
        self.log.debug(q_url)
        r = requests.get(q_url)
        return self.parse_response(r)
