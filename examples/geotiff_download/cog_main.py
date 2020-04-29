##########################################################################
# Cog Main
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
import json
import argparse
import logging
import logging.config

from lib.workflow_lib import get_cog_multiband_download_links
from lib.cog_raster_lib import CogRasterLib


def main(args):
    log = logging.getLogger(__name__)
    # Input Parameter
    input_tif = args.input_tif
    output_dir = args.output_dir
    validate_terravion_cog = args.validate_terravion_cog
    block_id_list = args.block_id_list
    block_name = args.block_name
    add_start_date = args.add_start_date
    # add_end_date = args.add_end_date
    product = args.product
    no_clipping = args.no_clipping
    dynamic = args.dynamic
    start_date = args.start_date
    end_date = args.end_date
    get_layers = args.get_layers
    get_summary = args.get_summary
    access_token = args.access_token

    # Create output dir if it doesnt already exist
    if output_dir is not None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    if validate_terravion_cog and input_tif:
        if CogRasterLib().validate_terravion_cog(input_tif):
            log.info('%s is a valid terravion cog', input_tif)
        else:
            log.info('%s is not a valid terravion cog', input_tif)

    elif (get_summary or get_layers) and access_token:
        get_cog_multiband_download_links(
            access_token,
            block_name=block_name,
            block_id_list=block_id_list,
            start_date=start_date,
            end_date=end_date,
            add_start_date=add_start_date,
            output_dir=output_dir,
            print_summary=get_summary,
            no_clipping=no_clipping,
            product=product,
            dynamic=dynamic)
    else:
        parser.print_help()


if __name__ == '__main__':
    argument_sample = 'Example: python ' + os.path.basename(os.path.realpath(__file__)) + \
        ' --access_token <access_token> --output_dir <output_dir> --block_id_list <block_id> '

    parser = argparse.ArgumentParser(description=argument_sample)

    parser.add_argument('--validate_terravion_cog', help='validate_terravion_cog',
                        action='store_true')
    parser.add_argument('--get_layers', help='get_layers',
                        action='store_true')
    parser.add_argument('--get_summary', help='get_summary',
                        action='store_true')
    parser.add_argument('--no_clipping', help='no_clipping',
                        action='store_true')
    parser.add_argument('--dynamic', help='Flag for enabling dynamic colormap for NDVI or Thermal products',
                        action='store_true')

    # parameters
    parser.add_argument('--access_token', help='access_token',
                        nargs='?', default=None)
    parser.add_argument('--block_id_list', help='block_id_list',
                        nargs='+', default=None)
    parser.add_argument('--block_name', help='block_name <name>',
                        nargs='?', default=None)
    parser.add_argument('--add_start_date', help='add start_date YY-MM-DD',
                        nargs='?', default=None)
    # parser.add_argument('--add_end_date', help='add end_date YY-MM-DD',
    #                     nargs='?', default=None)
    parser.add_argument('--start_date', help='capture start_date YY-MM-DD',
                        nargs='?', default=None)
    parser.add_argument('--end_date', help='capture end_date YY-MM-DD',
                        nargs='?', default=None)
    parser.add_argument('--product', help='product => MULTIBAND [default], SYNTHETIC_NC, NC, NDVI, CIR, THERMAL',
                        nargs='?', default=None)
    parser.add_argument('--input_tif', help='input_tif',
                        nargs='?', default=None)
    parser.add_argument('--output_dir', help='output_dir',
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
