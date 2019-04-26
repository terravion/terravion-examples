


import os
import requests
import json
import datetime
import argparse
from os.path import basename

class LatLngToCOG:
    def __init__(self, access_token, lat, lng):
        self.access_token = access_token
        self.api2_domain = 'https://api2.terravion.com/'
        self.lat = lat
        self.lng = lng
        self.user_id = None
        self.CLIP_BOUNDARY = True
    def parse_response(self, r):
        if r.status_code == 200:
            print('-----------------Response-------------------')
            print(json.dumps(r.json(), sort_keys=True, indent=2))
            print('------------------------------------')
            result = r.json()
            return result
        else:
            print('error:' + str(r.status_code))
            print(r.text)
            print('-------------------------------------------------------')
    def get_user_id(self):
        q_url = self.api2_domain
        q_url += 'users/getUserId?'
        q_url += '&access_token=' + self.access_token
        print(q_url)
        r = requests.get(q_url)
        return self.parse_response(r)
    def get_layers(self):
        print('get_layers')
        q_url = self.api2_domain
        q_url += 'users/'+ self.user_id +'/getLayers?'
        q_url += 'access_token=' + self.access_token
        q_url += '&lat=' + str(self.lat)
        q_url += '&lng=' + str(self.lng)
        print(q_url)
        r = requests.get(q_url)
        return self.parse_response(r)
    def get_geom(self, block_id):
        print('get_geom')
        q_url = self.api2_domain
        q_url += 'blocks/' + block_id
        q_url += '/geom.geojson?&access_token=' + self.access_token
        print(q_url)
        r = requests.get(q_url)
        return self.parse_response(r)
    def download_cog_from_s3(self, s3_url, outfile, epsg=4326, geojson_string=None, working_dir=None):
        gdalwarp_cmd_list = [
            'gdalwarp',
            '--config GDAL_CACHEMAX 500',
            '-wm 500',
            '-co BIGTIFF=YES',
            '--config GDALWARP_IGNORE_BAD_CUTLINE YES',
            '-t_srs EPSG:'+ str(epsg),
            '-of GTiff',
        ]
        if self.CLIP_BOUNDARY:
            gdalwarp_cmd_list.append('-crop_to_cutline -cutline')
            if geojson_string:
                gdalwarp_cmd_list.append("'"+ geojson_string+ "'")
            else:
                raise Exception('Need to supply geojson_string')

        if not outfile:
            outfile = '<OUTFILE>'
        gdalwarp_cmd_list += [
            '/vsicurl/'+ s3_url.replace('s3://', 'https://s3-us-west-2.amazonaws.com/'),
            outfile
        ]

        gdalwarp_cmd = ' '.join(gdalwarp_cmd_list)
        if working_dir:
            print(str(gdalwarp_cmd))
            os.system(gdalwarp_cmd)
        else:
            print(str(gdalwarp_cmd))
    def get_cogs(self, working_dir):

        self.user_id = self.get_user_id()
        layers = self.get_layers()
        if layers:
            for layer in layers:
                print(json.dumps(layer, sort_keys=True, indent=2))
                outfile = None
                if working_dir:
                    layer_date = datetime.datetime.utcfromtimestamp(layer['layerDateEpoch']).strftime('%Y-%m-%d')
                    outfile = os.path.join(working_dir, layer_date + '_' + layer['blockId'] + 'tif')
                geom = json.dumps(self.get_geom(layer['blockId']))
                self.download_cog_from_s3(layer['cogUrl'], outfile,
                    epsg=4326, geojson_string=geom, working_dir=working_dir)
def main(args):
    lat = args.lat
    lng = args.lng
    access_token = args.access_token
    working_dir = args.working_dir
    if lat and lng and access_token:
        ll2cog = LatLngToCOG(access_token, lat, lng)
        ll2cog.get_cogs(working_dir)
    else:
        parser.print_help()

if __name__ == '__main__':
    argument_sample = 'python ' + basename(os.path.realpath(__file__)) + \
        ' --lat <lat> --lng <lng> --access_token <access_token>'
    parser = argparse.ArgumentParser(description=argument_sample)

    # parameters
    parser.add_argument('--access_token', help='access_token',
                        nargs='?', default=None)
    parser.add_argument('--lat', help='lat',
                        nargs='?', default=None)
    parser.add_argument('--lng', help='lng',
                        nargs='?', default=None)
    parser.add_argument('--working_dir', help='working_dir',
                        nargs='?', default=None)
    args = parser.parse_args()
    main(args)