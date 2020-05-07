import json
import logging
import requests

from util import config


# List of commonly used colormaps by name
color_map_list = [
    'N-GREENG', 'N-R2', 'N-R3', 'T', 'N-AVHRR', 'JG', 'BW',
    'RW-LEGACY', 'GRANULAR', 'GM-COMP1', 'GM-RGB3', 'GM-QUAD',
    'CVC', 'CHS_HC2', 'CHS_HC1', 'SMWE', '10 Class Agroprecision Grey',
    '6 Class Agroprecision', '6 Class Agroprecision Grey',
    '10 Class Agroprecision', 'CHS-LEGACY', 'TRICOLOR', 'TWE'
]


class TerrAvionAPI2Colormap:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.api2_domain = config.api2_domain

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

    def get_colormap(self, colormap_id=None, colormap_name=None, output_format='terravion'):
        q_url = self.api2_domain

        if colormap_id:
            q_url += 'colormaps/' + colormap_id

        if colormap_name:
            filter_dict = {"where": {"name": colormap_name}}
            q_url += 'colormaps?filter=' + str(json.dumps(filter_dict))

        self.log.debug(q_url)

        r = requests.get(q_url)

        response = self.parse_response(r)

        if isinstance(response, list):
            response = response[0]

        if output_format == 'terravion':
            return response['lookup']
        elif output_format == 'rasterio':
            return self.to_rasterio_format(response['lookup'])
        else:
            self.log.error('Invalid output_format: %s', str(output_format))
            return None

    def to_rasterio_format(self, lookup):
        colormap = {}

        for i, d in enumerate(lookup):
            colormap[i] = (d['r'], d['g'], d['b'])

        return colormap
