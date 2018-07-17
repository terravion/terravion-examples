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
import sys
import urllib
import requests
import csv
import re
import argparse
from os.path import basename
from urllib2 import Request, urlopen, URLError, HTTPError
import datetime
import time
from datetime import datetime
import json
import traceback
requests.packages.urllib3.disable_warnings()
# Contact wmaio@terravion.com for access_token
# Access_token
# Pleaese modify the product_name to download the perspective product
'''
    NC => RGB
    CIR => Color Infrared
    NDVI => NDVI
    TIRS => Thermal
    ZONE => Zoning
    FULL => all of the above
'''

'''
    NDVI Color Map Options:

    N-R3 => TerrAvion Default - This scale is based on the Historic TerrAvion color pallet and is very tightly focused on the range most relevant to variation in vines and similar crops.
    N-R2 => TerrAvion Wide Range - This pallet uses the same colors as the TerrAvion Default scale, but the range of variation is larger, it may be of use when looking at changes over a very long time as it will call out seasonal changes in bigger color blocks.
    N-AVHR => AVHRR Scale - Based on the scle of the NASA Earth imaging mission, this scale is a finely graded to categorize variation into many different gradations.
    Green Gradient - A continuous scale from black to bright green, this scale show the data in a monochrome scale which does not bin any pixel.  Each pixel value is a unique color brightness.  This scale may make categorization hard, but you can see the full sensitivity of the NDVI.
    N => TerrAvion Historic - This is the pallet we provided at the beginning of the season, it is provided for comparison and continuity purposes.  It is useful in looking at extreme changes in vigor.
'''

generate_csv = True
timeout_seconds = 7200  # 2 hours
beta_server = 'http://ec2-54-148-188-230.us-west-2.compute.amazonaws.com:8123'

'''
This beta version of the code creates all of the requests upfront
    and retrieves after the imagery is ready for download.

'''


# Creating the folder if it does not exist
def main(argv):
    argument_sample = 'python ' + basename(os.path.realpath(__file__)) + \
        ' -working_dir <working_dir> -year_week <year_week> -product_name <product_name> -access_token <access_token> -product_name <product_name>'

    parser = argparse.ArgumentParser(description=argument_sample)

    parser.add_argument('-working_dir', help="working_dir",
                        nargs='?', default=None)

    parser.add_argument('-year_week', help='year_week get leayrs in given year_week',
                        nargs='?', default=None)

    parser.add_argument('-username', help='username',
                        nargs='?', default=None)

    parser.add_argument('-access_token', help='access_token',
                        nargs='?', default=None)

    parser.add_argument('-product_name', help='product_name NC,CIR,NDVI,ZONE,TIRS,MULTIBAND FULL',
                        nargs='?', default=None)

    parser.add_argument('-color_map', help='color_map N-AVHRR N-R3 N-R2 N-GREENG',
                        nargs='?', default='N-AVHRR')

    parser.add_argument('-task_list', help='task_list',
                        nargs='?', default=None)

    parser.add_argument('-RGB_color_map', help='RGB_color_map',
                        nargs='?', default=None)

    parser.add_argument('-output_csv', help='output_csv filename',
                        nargs='?', default=None)

    parser.add_argument('-error_only_logging', help='error_only_logging',
                        nargs='?', default=True)

    parser.add_argument('-rolling_window', help='rolling_window',
                        nargs='?', default=None)

    parser.add_argument('-rollback_start_days', help='rollback_start_days',
                        nargs='?', default=1)

    parser.add_argument('-sub_folder_by_block_product', help='sub_folder_by_block_product',
                        nargs='?', default=None)

    parser.add_argument('-layer_id', help='layer_id',
                        nargs='?', default=None)

    # Optional Filters
    parser.add_argument('-ranch_name', help='ranch_name',
                        nargs='+', default=None)

    parser.add_argument('-order_id', help='order_id',
                        nargs='+', default=None)

    args = parser.parse_args()
    working_dir = args.working_dir
    year_week = args.year_week
    username = args.username
    product_name = args.product_name
    access_token = args.access_token
    color_map = args.color_map
    task_list = args.task_list
    RGB_color_map = args.RGB_color_map
    output_csv = args.output_csv
    error_only_logging = args.error_only_logging
    rolling_window = args.rolling_window
    rollback_start_days = int(args.rollback_start_days)
    sub_folder_by_block_product = args.sub_folder_by_block_product

    # Optional Filters
    layer_id = args.layer_id
    ranch_name_list = args.ranch_name
    order_id_list = args.order_id

    if not (username and access_token):
        print 'Pleaese include -username -access_token -working_dir'
        print 'email William Maio at wmaio@terravion.com if you need one'
        print parser.print_help()
        return 0

    if task_list and access_token:
        request_info = {}
        request_info['server_address'] = beta_server
        request_info['access_token'] = access_token
        request_url = '%(server_address)s/v1/layers/task_list/?access_token=%(access_token)s' % request_info
        print request_url

        request = Request(request_url)
        response_body = urlopen(request).read()
        # print response_body
        task_list = json.loads(response_body)

        for task in task_list:
            print task

        return True

    elif layer_id:
        print 'TODO invoke downoad request by layer_id'

    elif rolling_window and rollback_start_days is not None and working_dir:
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        download_imagery_rw_deamon(
            working_dir, username, access_token, rollback_start_days,
            color_map, sub_folder_by_block_product=sub_folder_by_block_product)

    elif not year_week:
        print '--------------------------------------------------------------------------------------------------------------------------------'
        block_dic_struct = get_block_list_with_id(username, access_token)

        if not product_name:
            product_name = 'NDVI'

        layer_list = get_all_layers_list(
            block_dic_struct, product_name, username, access_token)

        # organize layers by week:
        week_year_dic = {}

        for layer in layer_list:
            date_object = datetime.strptime(layer['layerdate'],
                                            "%Y-%m-%dT%H:%M:%S.%fZ")

            week_year_index = str(
                date_object.isocalendar()[0]) + '_' + \
                "%02d" % date_object.isocalendar()[1]

            if week_year_index not in week_year_dic:
                week_dic = {}
            else:
                week_dic = week_year_dic[week_year_index]

            week_dic[layer['block_id']] = layer
            week_year_dic[week_year_index] = week_dic

        for week_year_index in sorted(week_year_dic.keys()):
            ranch_list = []

            for block_id in week_year_dic[week_year_index]:
                ranch_name = week_year_dic[week_year_index][block_id]['block_name'].split('/')[0]

                if ranch_name not in ranch_list:
                    ranch_list.append(ranch_name)

            print week_year_index, datetime.strptime(week_year_index + '-0', "%Y_%W-%w").strftime('%Y-%m-%d'), sorted(ranch_list)

        print '--------------------------------------------------------------------------------------------------------------------------------'
        print parser.print_help()
        print '--------------------------------------------------------------------------------------------------------------------------------'

    elif not working_dir:
        print 'pleaese include -working_dir'
        print '--------------------------------------------------------------------------------------------------------------------------------'
        print parser.print_help()
        print '--------------------------------------------------------------------------------------------------------------------------------'

    elif not product_name or product_name not in ['NC', 'CIR', 'NDVI', 'ZONE', 'TIRS', 'MULTIBAND', 'FULL']:
        print 'pleaese include valid -product_name [NC,CIR,NDVI,ZONE,TIRS,MULTIBAND,FULL]'
        print '--------------------------------------------------------------------------------------------------------------------------------'
        print parser.print_help()
        print '--------------------------------------------------------------------------------------------------------------------------------'

    elif product_name:
        if generate_csv and not output_csv:
            output_csv = os.path.join(
                working_dir,
                datetime.now().strftime('%Y-%m-%d_%H:%M:%S') +
                '_' + year_week + '_' + product_name + '.csv')

        downloading_report = DownloadingReport(csv_filename=output_csv)
        print 'download imagery', year_week

        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        block_dic_struct = get_block_list_with_id(username, access_token)
        product_name_list = []

        if product_name == 'FULL':
            product_name_list = ['NC', 'CIR', 'NDVI', 'ZONE', 'TIRS']
        else:
            product_name_list = [product_name]

        for product_name in product_name_list:
            run_download_workflow(
                downloading_report, working_dir, year_week, product_name,
                block_dic_struct, username, access_token, color_map,
                RGB_color_map, error_only_logging)

        if downloading_report.csv_filename:
            downloading_report.write_csv_file()
        else:
            downloading_report.print_download_record_list()

    else:
        print '--------------------------------------------------------------------------------------------------------------------------------'
        print parser.print_help()
        print '--------------------------------------------------------------------------------------------------------------------------------'


def download_imagery_rw_deamon(working_dir, username, access_token,
                               rollback_start_days, color_map,
                               sub_folder_by_block_product=None):
    print '--------------------------------------------------------------------------------------------------------------------------------'
    addEpochStart = int(datetime.now().strftime("%s")) - \
        rollback_start_days * 24 * 60 * 60
    addEpochEnd = int(datetime.now().strftime("%s"))

    # addEpochStart=int(datetime.now().strftime("%s"))
    # subtract one hour
    # addEpochEnd=int(datetime.now().strftime("%s"))-60*60
    print addEpochStart, addEpochEnd

    while True:
        block_dic_struct = get_block_list_with_id(username, access_token)
        product_name_list = ['NC', 'CIR', 'NDVI', 'ZONE', 'TIRS']
        master_layer_list = []

        for product_name in product_name_list:
            layer_list = get_layer_by_add_date(
                block_dic_struct, product_name, username,
                access_token, addEpochStart, addEpochEnd)

            master_layer_list = master_layer_list + layer_list

        if master_layer_list:
            request_info_list = []

            for layer_info in master_layer_list:
                if sub_folder_by_block_product:
                    clean_block_name = clean_filename(
                        layer_info['block_name'] + '_' + layer_info['product'])

                    working_sub_dir = os.path.join(
                        working_dir, clean_block_name)

                    if not os.path.exists(working_sub_dir):
                        os.makedirs(working_sub_dir)

                    request_info = get_geotiff(
                        layer_info, layer_info['product_name'],
                        color_map, username, access_token,
                        working_sub_dir,
                        include_block_id_flag=True,
                        RGB_color_map=None)
                else:
                    request_info = get_geotiff(
                        layer_info, layer_info['product_name'],
                        color_map, username, access_token, working_dir,
                        include_block_id_flag=True, RGB_color_map=None)

                print 'response_info', request_info
                request_info_list.append(request_info)

            while True:
                pending_request_info_list = []

                for request_info in request_info_list:
                    print request_info

                    try:
                        if 'status' not in request_info:
                            if 'output_filename' in request_info:
                                pending_request_info_list.append(request_info)
                            else:
                                request_info['status'] = 'ERROR'
                                request_info['message'] = 'status not in request_info'
                                request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                                report_error(request_info)
                                # downloading_report.insert_download_result(request_info)

                        elif request_info['status'] in ('INPROGRESS', 'INITIAL'):
                            pending_request_info_list.append(request_info)

                        elif 'cached' in request_info:
                            print 'file already exisits in system', request_info['output_filename']
                            '''
                            if not error_only_logging:
                                request_info['timestamp']=datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                                downloading_report.insert_download_result(request_info)
                            '''

                        elif 'download_url' in request_info:
                            try:
                                download_filename = request_info[
                                    'output_filename']

                                download_file(request_info['download_url'],
                                              download_filename)

                                request_info['status'] = 'SUCCESS'
                                request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

                                '''
                                if not error_only_logging:
                                    downloading_report.insert_download_result(request_info)
                                '''

                            except:
                                request_info['message'] = str(traceback.format_exc())
                                request_info['status'] = 'ERROR'
                                request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                                report_error(request_info)
                                # downloading_report.insert_download_result(request_info)

                        else:
                            print 'error', request_info
                            request_info['status'] = 'ERROR'
                            request_info['message'] = json.dumps(request_info)
                            request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                            report_error(request_info)
                            # downloading_report.insert_download_result(request_info)

                    except:
                        if not request_info:
                            request_info = {}

                        request_info['status'] = 'ERROR'
                        request_info['message'] = str(traceback.format_exc())
                        request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                        report_error(request_info)
                        # downloading_report.insert_download_result(request_info)

                time.sleep(5)
                request_info_list = []
                print 'pending requests', pending_request_info_list

                for pending_request in pending_request_info_list:
                    try:
                        request_info = check_request_update(pending_request,
                                                            username,
                                                            access_token)
                        request_info_list.append(request_info)

                    except:
                        request_info['status'] = 'ERROR'
                        request_info['message'] = str(traceback.format_exc())
                        request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                        report_error(request_info)
                        # downloading_report.insert_download_result(request_info)

                if not request_info_list:
                    print 'finished all request'
                    break

        print 'waiting 1 hour to request again'
        time.sleep(60 * 60)

        # rolling window one hour
        addEpochStart = int(datetime.now().strftime("%s")) - 2 * 60 * 60
        addEpochEnd = int(datetime.now().strftime("%s"))

        print 'new request and_start_date 2 hours eariler, add_end_date now, '


def run_download_workflow(downloading_report, working_dir, year_week,
                          product_name, block_dic_struct, username,
                          access_token, color_map, RGB_color_map,
                          error_only_logging):
    layer_list = get_all_layers_list(block_dic_struct, product_name,
                                     username, access_token)
    # organize layers by week:
    week_year_dic = {}

    for layer in layer_list:
        date_object = datetime.strptime(layer['layerdate'],
                                        "%Y-%m-%dT%H:%M:%S.%fZ")

        week_year_index = str(date_object.isocalendar()[0]) + \
            '_' + "%02d" % date_object.isocalendar()[1]

        if week_year_index not in week_year_dic:
            week_dic = {}
        else:
            week_dic = week_year_dic[week_year_index]

        week_dic[layer['block_id']] = layer
        week_year_dic[week_year_index] = week_dic

    if year_week in week_year_dic.keys():
        week_year_index = year_week

        include_block_id_flag = check_duplicate_block_name(
            week_year_dic[week_year_index])

        request_info_list = []

        for block_id in week_year_dic[week_year_index]:
            print 'requesting', week_year_dic[week_year_index][block_id]['block_name'], datetime.strptime(week_year_dic[week_year_index][block_id]['layerdate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')

            request_info = get_geotiff(
                week_year_dic[week_year_index][block_id],
                product_name, color_map, username, access_token, working_dir,
                include_block_id_flag, RGB_color_map=RGB_color_map)

            print 'response_info', request_info
            request_info_list.append(request_info)

        while True:
            pending_request_info_list = []

            for request_info in request_info_list:
                try:
                    if 'status' not in request_info:
                        if 'output_filename' in request_info:
                            pending_request_info_list.append(request_info)
                        else:
                            request_info['status'] = 'ERROR'
                            request_info['message'] = 'status not in request_info'
                            request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                            report_error(request_info)
                            downloading_report.insert_download_result(request_info)

                    elif request_info['status'] in ('INPROGRESS', 'INITIAL'):
                        pending_request_info_list.append(request_info)

                    elif 'cached' in request_info:
                        print 'file already exisits in system', request_info['output_filename']

                        if not error_only_logging:
                            request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                            downloading_report.insert_download_result(request_info)

                    elif 'download_url' in request_info:
                        try:
                            download_filename = request_info['output_filename']
                            download_file(request_info['download_url'],
                                          download_filename)

                            request_info['status'] = 'SUCCESS'
                            request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

                            if not error_only_logging:
                                downloading_report.insert_download_result(request_info)

                        except:
                            request_info['message'] = str(traceback.format_exc())
                            request_info['status'] = 'ERROR'
                            request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                            report_error(request_info)

                            downloading_report.insert_download_result(request_info)

                    else:
                        print 'error', request_info
                        request_info['status'] = 'ERROR'
                        request_info['message'] = json.dumps(request_info)
                        request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                        report_error(request_info)
                        downloading_report.insert_download_result(request_info)

                except:
                    if not request_info:
                        request_info = {}

                    request_info['status'] = 'ERROR'
                    request_info['message'] = str(traceback.format_exc())
                    request_info['timestamp'] = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                    report_error(request_info)
                    downloading_report.insert_download_result(request_info)

            time.sleep(5)
            request_info_list = []

            print 'pending requests', pending_request_info_list

            for pending_request in pending_request_info_list:
                try:
                    request_info = check_request_update(pending_request,
                                                        username,
                                                        access_token)
                    request_info_list.append(request_info)

                except:
                    request_info['status'] = 'ERROR'
                    request_info['message'] = str(traceback.format_exc())
                    request_info['timestamp'] = datetime.now(
                    ).strftime('%m/%d/%Y %H:%M:%S')
                    report_error(request_info)
                    downloading_report.insert_download_result(request_info)

            if not request_info_list:
                print 'finished all request'
                break

    else:
        print 'invalid week_year', week_year_index


def check_duplicate_block_name(block_dic):
    block_name_list = []
    block_id_list = []

    for block_id in block_dic:
        block_name_list.append(block_dic[block_id]['block_name'])
        block_id_list.append(block_id)

    if len(tuple(set(block_name_list))) == len(tuple(set(block_id_list))):
        return None
    else:
        return True


def get_all_layers_list(block_dic_struct, product_name,
                        username, access_token):
    if product_name in ('MULTIBAND', 'FULL'):
        product_name = 'NDVI'

    request_url = 'https://api.terravion.com/v1/users/' + username + \
        '/layers?product=' + product_name + '&access_token=' + access_token

    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    layer_list_json = json.loads(response_body)

    # Organize the layer_id with block_name
    layer_list = []

    for layer_info in layer_list_json:
        layer_struct = {}
        layer_struct['id'] = layer_info['id']
        layer_struct['layerdate'] = layer_info['layerDate']
        layer_struct['product'] = layer_info['product']
        layer_struct['block_id'] = layer_info['block']['id']
        layer_struct['block_name'] = block_dic_struct[layer_info['block']['id']]['block_name']
        layer_list.append(layer_struct)

    return layer_list


def get_layer_by_add_date(block_dic_struct, product_name, username,
                          access_token, addEpochStart, addEpochEnd):
    # addEpochStart=1457191383&addEpochEnd=1471047970&product=NC&access_token=849811e8-2fbe-4c3e-93e9-980b15a38426
    if product_name == 'MULTIBAND':
        product_name = 'NDVI'

    request_info = {}
    request_info['username'] = username
    request_info['product_name'] = product_name
    request_info['access_token'] = access_token
    request_info['addEpochStart'] = addEpochStart
    request_info['addEpochEnd'] = addEpochEnd
    request_url = 'https://api.terravion.com/v1/users/%(username)s/layers?addEpochStart=%(addEpochStart)s&addEpochEnd=%(addEpochEnd)s&product=%(product_name)s&access_token=%(access_token)s' % request_info
    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    layer_list_json = json.loads(response_body)
    # Organize the layer_id with block_name
    layer_list = []

    for layer_info in layer_list_json:
        layer_struct = {}
        layer_struct['id'] = layer_info['id']
        layer_struct['layerdate'] = layer_info['layerDate']
        layer_struct['product'] = layer_info['product']
        layer_struct['product_name'] = product_name
        layer_struct['block_id'] = layer_info['block']['id']
        layer_struct['block_name'] = block_dic_struct[layer_info['block']['id']]['block_name']
        layer_list.append(layer_struct)

    return layer_list


def get_layer_list(block_dic_struct):
    # Get the layer list of the users between the time period of start_date
    # and end_date and organize the layers by the block_name
    request_url = 'https://api.terravion.com/v1/users/' + \
        username + '/layers?epochStart=' + \
        str(start_date_epoc) + '&epochEnd=' + str(end_date_epoc) + \
        '&product=' + product_name + '&access_token=' + access_token

    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    layer_list_json = json.loads(response_body)

    # Organize the layer_id with block_name
    layer_list = []

    for layer_info in layer_list_json:
        print layer_info
        layer_struct = {}
        layer_struct['id'] = layer_info['id']
        layer_struct['layerdate'] = layer_info['layerDate']
        layer_struct['product'] = layer_info['product']
        layer_struct['block_id'] = layer_info['block']['id']
        layer_struct['block_name'] = block_dic_struct[layer_info['block']['id']]['block_name']
        layer_list.append(layer_struct)

    return layer_list


def get_user_colormap(username, access_token):
    request_url = 'https://api.terravion.com/v1/users/' + \
        username + '/?access_token=' + access_token

    request = Request(request_url)
    response_body = urlopen(request).read()
    user_info = json.loads(response_body)

    return user_info


def make_download_request(output_filename, access_token, layer_id,
                          product_name, color_map=None, RGB_color_map=None):
    request_info = {}
    request_info['access_token'] = access_token
    request_info['server_address'] = beta_server
    request_info['layer_id'] = layer_id

    if product_name == 'MULTIBAND':
        request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/multiband.tiff?access_token=%(access_token)s' % request_info

    elif 'NC' == product_name or 'CIR' == product_name:
        request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=null&access_token=%(access_token)s' % request_info

    elif 'TIRS' == product_name:
        if RGB_color_map:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=T&access_token=%(access_token)s&isColormapRgb=true' % request_info
        else:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=T&access_token=%(access_token)s' % request_info

    elif 'NDVI' == product_name or 'ZONE' == product_name:
        request_info['colorMap'] = urllib.quote(color_map)

        if RGB_color_map:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=%(colorMap)s&access_token=%(access_token)s&isColormapRgb=true' % request_info
        else:
            request_url = '%(server_address)s/v1/layers/%(layer_id)s/geotiffs/image.tiff?colorMap=%(colorMap)s&access_token=%(access_token)s' % request_info

    # print request_url
    # response_file = urlopen(request)

    try:
        print 'output_filename:', output_filename
        print 'request_url:', request_url
        r = requests.get(request_url)
        print r

        response_info = json.loads(r.content)
        response_info['output_filename'] = output_filename
        response_info['request_url'] = request_url
        time.sleep(1)

        return response_info

    except:
        if request_info:
            error_message = request_info
        else:
            error_message = {}

        error_message['request_url'] = request_url
        error_message['output_filename'] = output_filename
        error_message['status'] = 'ERROR'
        error_message['message'] = str(traceback.format_exc())

        print traceback.format_exc()

        return error_message


def get_geotiff(layer_info, product_name, color_map, username,
                access_token, working_dir, include_block_id_flag,
                RGB_color_map=None):
    # Download the product specified by the product and colormap to the working directory
    # http://docs.terravionv1.apiary.io/#reference/layers/usersuseridoremaillayerstileszxypngcolormapepochstartepochendproduct
    # print layer_info

    layer_id = layer_info['id']
    date_object = datetime.strptime(layer_info['layerdate'],
                                    "%Y-%m-%dT%H:%M:%S.%fZ")
    print layer_id

    if include_block_id_flag:
        output_filename = os.path.join(
            working_dir,
            layer_info['block_name'].replace('/', '_') +
            '_' + product_name + '_' + date_object.strftime('%Y-%m-%d') +
            '_' + layer_info['block_id'] + '.tif')
    else:
        output_filename = os.path.join(
            working_dir,
            layer_info['block_name'].replace('/', '_') +
            '_' + product_name +
            '_' + date_object.strftime('%Y-%m-%d') + '.tif')

    print output_filename, os.path.isfile(output_filename)

    if not os.path.isfile(output_filename):
        return make_download_request(output_filename, access_token, layer_id,
                                     product_name, color_map=color_map,
                                     RGB_color_map=RGB_color_map)
    else:
        request_info = {}
        request_info['cached'] = True
        request_info['status'] = 'SUCCESS'
        request_info['download_url'] = 'N/A'
        request_info['request_url'] = 'N/A'
        request_info['message'] = 'N/A'
        request_info['output_filename'] = output_filename

        return request_info


def check_request_update(request_info, username, access_token):
    output_filename = request_info['output_filename']
    request_url = request_info['request_url']

    request_info['access_token'] = access_token
    request_info['server_address'] = beta_server
    request_url = '%(server_address)s/v1/layers/task/?access_token=%(access_token)s&task_id=%(task_id)s' % request_info
    r = requests.get(request_url)
    print r.content

    request_info = json.loads(r.content)
    request_info['output_filename'] = output_filename
    request_info['request_url'] = request_url

    return request_info


def get_block_list_with_id(username, access_token):
    # Getting the list of blocks owned by the user

    # http://docs.terravionv1.apiary.io/#reference/users/user-blocks-collection/retrieve-blocks-user-has-access-to
    request_url = 'https://api.terravion.com/v1/users/' + \
        username + '/blocks' + '?access_token=' + access_token
    print request_url

    request = Request(request_url)
    response_body = urlopen(request).read()
    # print response_body

    block_list_json = json.loads(response_body)
    block_dic_struct = {}

    for block_info in block_list_json:
        block_struct = {}
        block_struct['block_name'] = str(block_info['block']['name'].encode("ascii", "ignore").encode("utf-8"))
        block_struct['block_id'] = str(block_info['block']['id'])
        block_dic_struct[block_struct['block_id']] = block_struct

    return block_dic_struct


def check_download_progress(status_dic, p1):
    while True:
        time_elapsed = time.time() - status_dic['running_time']

        if status_dic['download_complete']:
            print 'check download thread complete'
            return True

        print time_elapsed, status_dic['download_complete']

        if time_elapsed > 120:  # if waiting for more than 2 mins then kill it and retry
            print 'download stuck'
            # kill both thread
            status_dic['kill_download_thread'] = True
            p1.terminate()
            # raise Exception('download stuck', 'finish thread')
            return True

        else:
            time.sleep(5)


def run_download_file(url, outfilename):
    r = requests.get(url, stream=True, timeout=timeout_seconds, verify=False)

    if r.status_code == 200:
        with open(outfilename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        raise Exception('status_code error', r.status_code)

    return outfilename


def download_file(url, outfilename):
    error_log_list = []
    download_try_limit = 5
    download_time_elapsed = 0
    download_complete = False
    kill_download_thread = False

    for attempt in range(download_try_limit):
        try:
            print 'download_url:', url
            print 'download_filename:', outfilename
            run_download_file(url, outfilename)

        except:
            # thread_a.stop()
            # thread_b.stop()
            print "download stuck?"
            error_log_list.append(str(traceback.format_exc()))

            if os.path.isfile(outfilename):
                os.remove(outfilename)

            continue

        if os.path.isfile(outfilename):
            return outfilename

    raise Exception('download failed', json.dumps(error_log_list))


def report_error(error_message):
    print error_message
    r = requests.put('%(beta_server)s/report_error/' % {
        'beta_server': beta_server},
        json={"message": error_message})

    print r, 'error message sent'


class DownloadingReport(object):

    def __init__(self, csv_filename=None):
        self.csv_filename = csv_filename
        self.csv_header_list = ['output_filename', 'status',
                                'request_url', 'download_url',
                                'timestamp', 'message']
        self.download_record_list = []

    def insert_download_result(self, download_record):
        self.download_record_list.append(download_record)

    def write_csv_file(self, csv_filename=None):
        if csv_filename and not self.csv_filename:
            self.csv_filename = output_csv

        if self.download_record_list:
            with open(self.csv_filename, 'wb') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(self.csv_header_list)

                for download_record in self.download_record_list:
                    output_filename = None
                    status = None
                    download_url = None
                    message = None
                    timestamp = None
                    request_url = None

                    if 'output_filename' in download_record:
                        output_filename = download_record['output_filename']

                    if 'status' in download_record:
                        status = download_record['status']

                    if 'download_url' in download_record:
                        download_url = download_record['download_url']

                    if 'message' in download_record:
                        message = download_record['message']

                    if 'timestamp' in download_record:
                        timestamp = download_record['timestamp']

                    if 'request_url' in download_record:
                        request_url = download_record['request_url']

                    csv_writer.writerow(
                        [output_filename, status,
                         request_url, download_url, timestamp,
                         message.replace('\n', ' ').replace('\r', '')])

    def print_download_record_list(self):
        if self.download_record_list:
            print '---------------------------------------------------------------------------------------'
            print ' '.join(self.csv_header_list)

            for download_record in self.download_record_list:
                output_filename = None
                status = None
                download_url = None
                message = None
                timestamp = None
                request_url = None

                if 'output_filename' in download_record:
                    output_filename = download_record['output_filename']

                if 'status' in download_record:
                    status = download_record['status']

                if 'download_url' in download_record:
                    download_url = download_record['download_url']

                if 'message' in download_record:
                    message = download_record['message']

                if 'timestamp' in download_record:
                    timestamp = download_record['timestamp']

                if 'request_url' in download_record:
                    request_url = download_record['request_url']

                print output_filename, status, download_url, timestamp, message


def clean_filename(filename):
    return re.sub("[!|*'();:@&=+$,/?# [\]]", '-', filename)


if __name__ == '__main__':
    main(sys.argv[1:])
