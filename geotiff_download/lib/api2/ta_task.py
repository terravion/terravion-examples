import json
import logging
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2Task:
    def __init__(self, user_id, access_token):
        self.access_token = access_token
        self.user_id = user_id
        self.api2_domain = config.api2_domain
    def request_geotiff_task(self, layer_id, multiband=None,
        geotiff_epsg=None, colormap=None):
        q_url = self.api2_domain
        if self.user_id and layer_id:
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
            logging.info(q_url)
        else:
            return None
        r = requests.post(q_url)
        logging.info('status code'+str(r.status_code))
        if r.status_code == 200:
            result = r.json()
            if result:
                logging.info('result'+json.dumps(result))
                return result
            else:
                return None
        else:
            return None

    def get_task_info(self, task_id):
        q_url = self.api2_domain
        if task_id:
            q_url += 'tasks/' + task_id
            q_url += '?access_token=' + self.access_token
            logging.info(q_url)
        else:
            return None
        r = requests.get(q_url)
        logging.info('status code'+str(r.status_code))
        if r.status_code == 200:
            result = r.json()
            if result:
                return result
            else:
                return None
        else:
            return None
