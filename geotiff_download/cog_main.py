##########################################################################
# Validate Download Cog
#
# This material contains sample programming source code ("Sample Code").
# TerrAvion grants you a nonexclusive license to compile, link, run,
# prepare derivative works of this Sample Code.  The Sample Code has not
# been thoroughly tested under all conditions.  TerrAvion, therefore, does
# not guarantee or imply its reliability, serviceability, or function.
#
# All Sample Code contained herein is provided to you "AS IS" without
# any warranties of any kind. THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGMENT ARE EXPRESSLY
# DISCLAIMED.  SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF IMPLIED
# WARRANTIES, SO THE ABOVE EXCLUSIONS MAY NOT APPLY TO YOU.  IN NO
# EVENT WILL TERRAVION BE LIABLE TO ANY PARTY FOR ANY DIRECT, INDIRECT,
# SPECIAL OR OTHER CONSEQUENTIAL DAMAGES FOR ANY USE OF THE SAMPLE CODE
# INCLUDING, WITHOUT LIMITATION, ANY LOST PROFITS, BUSINESS
# INTERRUPTION, LOSS OF PROGRAMS OR OTHER DATA ON YOUR INFORMATION
# HANDLING SYSTEM OR OTHERWISE, EVEN IF WE ARE EXPRESSLY ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGES.
#
# COPYRIGHT
# ---------
# (C) Copyright TerrAvion Inc. 2019
# All rights reserved.
#
#
# AUTHOR
# ------
# William Maio
# wmaio@terravion.com
# http://www.terravion.com
#
##########################################################################

import os
import rasterio
import json
import argparse
import logging
import logging.config
from os.path import basename
from lib.cog_raster_lib import CogRasterLib
from lib.api2.ta_layer import TerrAvionAPI2Layer
from lib.api2.ta_block import TerrAvionAPI2Block
def main(args):
    log = logging.getLogger(__name__)
    # Input Parameter
    input_tif = args.input_tif
    working_dir = args.working_dir
    validate_terravion_cog = args.validate_terravion_cog
    block_id = args.block_id
    layer_date = args.layer_date
    get_layers = args.get_layers
    user_id = args.user_id
    access_token = args.access_token
    if validate_terravion_cog and input_tif:
        cr_lib = CogRasterLib()
        if cr_lib.validate_terravion_cog(input_tif):
            log.info('%s is a valid terravion cog', input_tif)
        else:
            log.info('%s is not a valid terravion cog', input_tif)
    elif get_layers and user_id and access_token:
        cr_lib = CogRasterLib()
        tapi2_layer = TerrAvionAPI2Layer(user_id, access_token, use_beta=True)
        tapi2_block = TerrAvionAPI2Block(access_token)
        layers = tapi2_layer.get_layers()
        for layer in layers:
            log.info(json.dumps(layer, indent=2, sort_keys=True))
            block_id = layer['blockId']
            block_info = tapi2_block.get_geom(block_id)
            log.info(json.dumps(block_info))
            cr_lib.download_cog_from_s3(layer['cogUrl'], epsg=4326, geojson_string=json.dumps(block_info), working_dir=working_dir)
    else:
        parser.print_help()

if __name__ == '__main__':
    argument_sample = 'python ' + basename(os.path.realpath(__file__)) + \
        ' --input_tif '
    parser = argparse.ArgumentParser(description=argument_sample)
    # flags
    parser.add_argument('--validate_terravion_cog', help='validate_terravion_cog',
                        action='store_true')
    parser.add_argument('--get_layers', help='get_layers',
                        action='store_true')

    # parameters

    parser.add_argument('--user_id', help='user_id',
                        nargs='?', default=None)
    parser.add_argument('--access_token', help='access_token',
                        nargs='?', default=None)
    parser.add_argument('--block_id', help='block_id',
                        nargs='?', default=None)
    parser.add_argument('--layer_date', help='layer_date',
                        nargs='?', default=None)
    parser.add_argument('--input_tif', help='input_tif',
                        nargs='?', default=None)
    parser.add_argument('--working_dir', help='working_dir',
                        nargs='?', default=None)
    parser.add_argument('-l', '-log', '--log', type=str,
                        default='INFO', help='Input log level')
    log_level_dict = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': 0
    }
    args = parser.parse_args()
    # Get log level value from log_level_dict lookup
    log_level = log_level_dict[args.log.upper()]
    logging.basicConfig(level=log_level)
    main(args)
