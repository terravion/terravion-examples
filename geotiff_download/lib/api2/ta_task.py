import json
import requests
import datetime
import traceback
import util.config as config
class TerrAvionAPI2Task:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api2_domain = config.api2_domain
    def request_geotiff_task(self, user_id, layer_id, multiband=True):
        q_url = self.api2_domain
        if user_id and layer_id:
            q_url += 'tasks/requestGeotiffTask'
            q_url += '?userId=' + user_id
            q_url += '&layerId=' + layer_id
            if multiband:
                q_url += '&multiband=true'
            q_url += '&access_token=' + self.access_token
            print q_url
        else:
            return None
        r = requests.post(q_url)
        print 'status code', r.status_code
        if r.status_code == 200:
            result = r.json()
            if result:
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
