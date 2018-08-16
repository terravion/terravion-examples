import json
import requests
import datetime
import traceback
import util.config as config

class TerrAvionAPI1Layer:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api1_domain = config.api1_domain
    def get_layers(self, user_email, product_name, epoch_start, epoch_end=None):
        # addEpochStart=1457191383&addEpochEnd=1471047970&product=NC&access_token=849811e8-2fbe-4c3e-93e9-980b15a38426
        if product_name == 'MULTIBAND':
            product_name = 'NDVI'
        q_url = self.api1_domain
        q_url += 'users/' + user_email
        q_url += '/layers?product=' + product_name
        if epoch_start:
            q_url += '&addEpochStart=' + str(epoch_start)
        if epoch_end:
            q_url += '&addEpochEnd=' + str(epoch_end)
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