import os
import json
import datetime
import time

from lib.api1.ta_user import TerrAvionAPI1User
from lib.api2.ta_block import TerrAvionAPI2Block
from lib.api2.ta_user_block import TerrAvionAPI2UserBlock
from lib.api2.ta_layer import TerrAvionAPI2Layer
from lib.api2.ta_task import TerrAvionAPI2Task


def date_to_epoch(date_string):
    if date_string:
        return int(datetime.datetime.strptime(date_string, "%Y-%m-%d").strftime('%s'))

def get_download_links(user_name, access_token, block_name=None,
    lat=None, lng=None, block_id_list=None, start_date=None, end_date=None,
    add_start_date=None, geotiff_epsg=None, product=None):
    print(user_name, access_token, block_name, lat, lng, block_id_list)

    ta1_user = TerrAvionAPI1User(access_token)
    user_info = ta1_user.get_user(user_name)
    user_id = user_info['id']

    ta2_layer = TerrAvionAPI2Layer(user_id, access_token,
        epoch_start=date_to_epoch(start_date),
        epoch_end=date_to_epoch(end_date),
        add_epoch_start=date_to_epoch(add_start_date))
    layer_info_list = []
    if (lat and lng):
        layer_info_list = ta2_layer.get_layers_by_lat_lng(lat=lat, lng=lng)
    elif block_id_list:
        layer_info_list = ta2_layer.get_layers_by_block_id_list(block_id_list)
    else:
        layer_info_list = ta2_layer.get_layers(field_name=block_name)
    if not layer_info_list:
        print('no layers found')
        return None
    print('found ',len(layer_info_list),'layers')
    ta2_task = TerrAvionAPI2Task(user_id, access_token)
    task_info_list = request_geotiff_tasks(ta2_task, layer_info_list, geotiff_epsg, product)
    download_url_list = check_tasks_until_finish(task_info_list, ta2_task)
    return download_url_list

def check_tasks_until_finish(task_info_list, ta2_task):
    download_url_list = []
    new_task_info_list = []
    while True:
        if task_info_list:
            print(len(task_info_list), 'tasks remaining')
        for task_info in task_info_list:
            task_response = ta2_task.get_task_info(task_info['task_id'])
            download_url = get_finished_download_link(task_response)
            if download_url:
                task_info['download_url'] = download_url
                download_url_list.append(task_info)
            else:
                new_task_info_list.append(task_info)
        if not new_task_info_list:
            break
        task_info_list = new_task_info_list
        new_task_info_list = []
        time.sleep(1)
    return download_url_list

def get_finished_download_link(task_info):
    if not task_info:
        return None
    elif not 'status' in task_info:
        return None
    elif not task_info['status'] == 'DONE':
        return None
    elif not 'response' in task_info:
        return None
    elif 'download_url' in task_info['response']:
        return task_info['response']['download_url']

def request_geotiff_tasks(ta2_task, layer_info_list, geotiff_epsg=None, product='MULTIBAND'):
    task_info_list = []
    for layer_info in layer_info_list:
        if product == 'MULTIBAND' and layer_info['ndviLayerId']:
            layer_id = layer_info['ndviLayerId']
            task_info = ta2_task.request_geotiff_task(layer_id, multiband=True,
                geotiff_epsg=geotiff_epsg)
            if task_info:
                task_info['product'] = 'MULTIBAND' 
                task_info['addDateEpoch'] = layer_info['addDateEpoch']
                task_info['layerDateEpoch'] = layer_info['layerDateEpoch']
                task_info['blockId'] = layer_info['blockId']
                if 'task_id' in task_info:
                    task_info_list.append(task_info)
        else:
            product_info_list = []
            add_epoch = layer_info['addDateEpoch']
            layer_epoch = layer_info['layerDateEpoch']
            if product == 'FULL':
                product_info_list.append({'layer_id': layer_info['ncLayerId'], 'product': 'RGB'})
                product_info_list.append({'layer_id': layer_info['cirLayerId'], 'product': 'CIR'})
                product_info_list.append({'layer_id': layer_info['ndviLayerId'], 'product': 'NDVI'})
                product_info_list.append({'layer_id': layer_info['thermalLayerId'], 'product': 'THERMAL'})
            elif product == 'ALL':
                product_info_list.append({'layer_id': layer_info['ncLayerId'], 'product': 'RGB'})
                product_info_list.append({'layer_id': layer_info['cirLayerId'], 'product': 'CIR'})
                product_info_list.append({'layer_id': layer_info['ndviLayerId'], 'product': 'NDVI'})
                product_info_list.append({'layer_id': layer_info['thermalLayerId'], 'product': 'THERMAL'})
                product_info_list.append({'layer_id': layer_info['ndviLayerId'], 'product': 'MULTIBAND'})
            elif product == 'NC':
                product_info_list.append({'layer_id': layer_info['ncLayerId'], 'product': 'RGB'})
            elif product == 'CIR': 
                product_info_list.append({'layer_id': layer_info['cirLayerId'], 'product': 'CIR'})
            elif product == 'NDVI':
                product_info_list.append({'layer_id': layer_info['ndviLayerId'], 'product': 'NDVI'})
            elif product == 'TIRS':
                product_info_list.append({'layer_id': layer_info['thermalLayerId'], 'product': 'THERMAL'})
            for product_info in product_info_list:
                if product_info['product'] == 'MULTIBAND':
                    task_info = ta2_task.request_geotiff_task(product_info['layer_id'],
                        geotiff_epsg=geotiff_epsg, multiband=True)
                else:
                    task_info = ta2_task.request_geotiff_task(product_info['layer_id'],
                        geotiff_epsg=geotiff_epsg)
                task_info['product'] = product_info['product']
                task_info['addDateEpoch'] = add_epoch
                task_info['layerDateEpoch'] = layer_epoch
                task_info['blockId'] = layer_info['blockId']
                if 'task_id' in task_info:
                    task_info_list.append(task_info)
    return task_info_list


def donwload_imagery(access_token, working_dir, download_info_list):
    if not os.path.exists(working_dir):
        os.mkdir(working_dir)
    ta_b = TerrAvionAPI2Block(access_token)
    import util.file_util as file_util
    print(len(download_info_list), 'files to be downloaded')
    for download_info in download_info_list:
        print(download_info)
        block_info = ta_b.get_block(download_info['blockId'])
        field_name = file_util.clean_filename(block_info['name'])
        layer_date = datetime.datetime.utcfromtimestamp(download_info['layerDateEpoch'])
        layer_date_string = layer_date.strftime("%Y-%m-%d")
        root_name = layer_date_string 
        root_name += '_' + field_name + '_'
        root_name += download_info['product'] + '.tif'
        out_file = os.path.join(working_dir, root_name)
        print('url', download_info['download_url'])
        print('out_file', out_file)
        file_util.run_download_file(download_info['download_url'], out_file)
