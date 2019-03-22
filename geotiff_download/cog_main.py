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
def main(args):
    log = logging.getLogger(__name__)
    # Input Parameter
    input_tif = args.input_tif
    working_dir = args.working_dir
    download_cog = args.download_cog
    validate_terravion_cog = args.validate_terravion_cog
    if validate_terravion_cog and input_tif:
        cr_lib = CogRasterLib()
        if cr_lib.validate_terravion_cog(input_tif):
            log.info('%s is a valid terravion cog', input_tif)
        else:
            log.info('%s is not a valid terravion cog', input_tif)
    elif download_cog and working_dir:
        cr_lib = CogRasterLib()
        outfile = os.path.join(working_dir, 'cog.tif')
        # cr_lib.download_cog_from_s3(self, , s3_url, epsg=4326, geojson_file=None, geojson_string=None)
    else:
        parser.print_help()

if __name__ == '__main__':
    argument_sample = 'python ' + basename(os.path.realpath(__file__)) + \
        ' --input_tif '
    parser = argparse.ArgumentParser(description=argument_sample)
    # flags
    parser.add_argument('--validate_terravion_cog', help='validate_terravion_cog',
                        action='store_true')
    parser.add_argument('--download_cog', help='download_cog',
                        action='store_true')
    # parameters
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
