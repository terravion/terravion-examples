import os
import requests
import json
import datetime
import argparse

from lib.cog_raster_lib import CogRasterLib


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
        q_url += 'users/' + self.user_id + '/getLayers?'
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

    def get_cogs(self, output_dir):
        self.user_id = self.get_user_id()
        layers = self.get_layers()

        if layers:
            for layer in layers:
                print(json.dumps(layer, sort_keys=True, indent=2))
                outfile = None

                if output_dir:
                    layer_date = datetime.datetime.utcfromtimestamp(layer['layerDateEpoch']).strftime('%Y-%m-%d')
                    outfile = os.path.join(output_dir, layer_date + '_' + layer['blockId'] + 'tif')

                geom = json.dumps(self.get_geom(layer['blockId']))

                CogRasterLib().download_cog_from_s3(
                    s3_url=layer['cogUrl'],
                    outfile=outfile,
                    epsg=4326,
                    geojson_string=geom,
                    output_dir=output_dir)


def main(args):
    lat = args.lat
    lng = args.lng
    access_token = args.access_token
    output_dir = args.output_dir

    if lat and lng and access_token:
        ll2cog = LatLngToCOG(access_token, lat, lng)
        ll2cog.get_cogs(output_dir)
    else:
        parser.print_help()


if __name__ == '__main__':
    argument_sample = 'python ' + os.path.basename(os.path.realpath(__file__)) + \
        ' --lat <lat> --lng <lng> --access_token <access_token>'
    parser = argparse.ArgumentParser(description=argument_sample)

    # parameters
    parser.add_argument('--access_token', help='access_token',
                        nargs='?', default=None)
    parser.add_argument('--lat', help='lat',
                        nargs='?', default=None)
    parser.add_argument('--lng', help='lng',
                        nargs='?', default=None)
    parser.add_argument('--output_dir', help='output_dir',
                        nargs='?', default=None)

    args = parser.parse_args()
    main(args)
