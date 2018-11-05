##########################################################################
# TerrAvion Bulk Download Beta
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
# (C) Copyright TerrAvion Inc. 2016
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
from os.path import basename
import lib.workflow_lib as workflow_lib
from lib.api1.ta_user import TerrAvionAPI1User
from lib.api2.ta_user import TerrAvionAPI2User
from lib.api2.ta_user_block import TerrAvionAPI2UserBlock

logging.basicConfig(level=logging.INFO)

# Contact wmaio@terravion.com for access_token
# Access_token
# Pleaese modify the product_name to download the perspective product
'''
    NC => RGB
    CIR => Color Infrared
    NDVI => NDVI
    TIRS => Thermal
    FULL => all of the above
    ALL => all of the above + MULTIABND
'''

'''
    NDVI Color Map Options:

    N-R3 => TerrAvion Default - This scale is based on the Historic TerrAvion color pallet and is very tightly focused on the range most relevant to variation in vines and similar crops.
    N-R2 => TerrAvion Wide Range - This pallet uses the same colors as the TerrAvion Default scale, but the range of variation is larger, it may be of use when looking at changes over a very long time as it will call out seasonal changes in bigger color blocks.
    N-AVHR => AVHRR Scale - Based on the scle of the NASA Earth imaging mission, this scale is a finely graded to categorize variation into many different gradations.
    Green Gradient - A continuous scale from black to bright green, this scale show the data in a monochrome scale which does not bin any pixel.  Each pixel value is a unique color brightness.  This scale may make categorization hard, but you can see the full sensitivity of the NDVI.
    N => TerrAvion Historic - This is the pallet we provided at the beginning of the season, it is provided for comparison and continuity purposes.  It is useful in looking at extreme changes in vigor.
'''

timeout_seconds = 7200  # 2 hours
api_server = 'https://api2.terravion.com/'


def run_geotiff_download(user_name=None, access_token=None,
            working_dir=None, get_block_list= None,
            product=None,
            block_name=None, block_id_list=None, lat=None, lng=None,
            add_start_date=None,
            start_date=None, end_date= None,
            with_colormap=False, geotiff_epsg=None):
    log = logging.getLogger(__name__)
    if geotiff_epsg:
        if not geotiff_epsg.isdigit() or not len(geotiff_epsg) == 4:
            log.critical('invalid EPSG Code: '+str(geotiff_epsg))
            return False
    if not (user_name and access_token):
        log.critical('email api@terravion.com for access_token')
        log.critical(parser.print_help())
        return False
    elif product and (block_name or (lat and lng) or block_id_list or
        add_start_date or start_date or end_date):
        log.debug('downloading geotiffs')
        download_info_list = workflow_lib.get_download_links(user_name,
            access_token, block_name,
            lat, lng, block_id_list, start_date, end_date, add_start_date,
            geotiff_epsg, product=product, with_colormap=with_colormap)
        if download_info_list:
            if working_dir:
                workflow_lib.donwload_imagery(access_token, working_dir,
                    download_info_list)
            else:
                for download_info in download_info_list:
                    log.debug(json.dumps(download_info, sort_keys=True, indent=2))
        return True
    elif get_block_list:
        ta1_user = TerrAvionAPI1User(access_token)
        user_info = ta1_user.get_user(user_name)
        ta2_user_block = TerrAvionAPI2UserBlock(user_info['id'], access_token)
        user_block_list = ta2_user_block.get_user_blocks()
        log.info('block_id, name')

        for user_block in user_block_list:
            log.info(','.join([user_block['blockId'], user_block['fieldName']]))
        return True
# Creating the folder if it does not exist
def main(args):
    log = logging.getLogger(__name__)
    # Input Parameter
    user_name = args.user_name
    access_token = args.access_token
    working_dir = args.working_dir
    # Workflow Parameters
    get_block_list = args.get_block_list
    product = args.product

    # Optional Filters
    block_name = args.block_name
    block_id_list = args.block_id_list
    lat = args.lat
    lng = args.lng
    add_start_date = args.add_start_date
    start_date = args.start_date
    end_date = args.end_date
    with_colormap = args.with_colormap
    # Geotiff parameters
    geotiff_epsg = args.EPSG
    run_flag = run_geotiff_download(user_name=user_name, access_token=access_token,
        working_dir=working_dir, get_block_list= get_block_list,
        product=product, block_name=block_name,
        block_id_list=block_id_list, lat=lat, lng=lng,
        add_start_date=add_start_date,
        start_date=start_date, end_date=end_date,
        with_colormap=with_colormap, geotiff_epsg=geotiff_epsg)
    if not run_flag:
        log.info(parser.print_help())

if __name__ == '__main__':
    argument_sample = 'python ' + basename(os.path.realpath(__file__)) + \
        ' -working_dir <working_dir>  -access_token <access_token> '

    parser = argparse.ArgumentParser(description=argument_sample)

    parser.add_argument('-user_name', help='user_name',
                        nargs='?', default=None)

    parser.add_argument('-access_token', help='access_token',
                        nargs='?', default=None)
    parser.add_argument('-working_dir', help='working_dir',
                        nargs='?', default=None)

    # workflow parameters

    parser.add_argument('-get_block_list', help='get_block_list',
                        nargs='?', default=None)
    parser.add_argument('-product', help='NC, CIR, NDVI, TIRS, MULTIBAND, FULL, ALL',
                        nargs='?', default=None)

    # Optional Filters
    parser.add_argument('-block_name', help='block_name',
                        nargs='?', default=None)

    parser.add_argument('-lat', help='lat',
                        nargs='?', default=None)
    parser.add_argument('-lng', help='lng',
                        nargs='?', default=None)

    parser.add_argument('-block_id_list', help='block_id_list',
                        nargs='+', default=None)

    parser.add_argument('-add_start_date', help='add_start_date',
                        nargs='?', default=None)

    parser.add_argument('-start_date', help='start_date',
                        nargs='?', default=None)

    parser.add_argument('-end_date', help='end_date',
                        nargs='?', default=None)

    parser.add_argument('-with_colormap', help='with_colormap',
                        action='store_true')

    # geotiff parameters
    parser.add_argument('-EPSG', help='EPSG',
                        nargs='?', default=None)

    parser.add_argument('-l', '-log', '--log', type=str,
                        default='INFO', help='Input log level')
    log_level_dict = {
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10,
        'NOTSET': 0
    }
    args = parser.parse_args()
    # Get log level value from log_level_dict lookup
    log_level = log_level_dict[args.log.upper()]
    logger = logging.getLogger()
    logger.setLevel(log_level)
    main(args)
