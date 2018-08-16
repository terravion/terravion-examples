import datetime
import time
from lib.api1.ta_user import TerrAvionAPI1User
from lib.api2.ta_user import TerrAvionAPI2User
from lib.api2.ta_user_block import TerrAvionAPI2UserBlock
from lib.api1.ta_layer import TerrAvionAPI1Layer
from lib.api2.ta_layer import TerrAvionAPI2Layer
from lib.api2.ta_task import TerrAvionAPI2Task


def get_multiband_download_links(user_name, access_token, block_name,
    lat, lng, block_id_list, start_date=None, end_date=None, add_start_date=None):
    print user_name, access_token, block_name, lat, lng, block_id_list

    ta1_user = TerrAvionAPI1User(access_token)
    ta1_layer = TerrAvionAPI1Layer(access_token)
    ta2_user_block = TerrAvionAPI2UserBlock(access_token)
    ta2_layer = TerrAvionAPI2Layer(access_token)
    ta2_task = TerrAvionAPI2Task(access_token)

    user_info = ta1_user.get_user(user_name)
    user_id = user_info['id']
    if block_name:
        block_id_list = get_block_id_list_from_block_name(user_id, block_name, ta2_user_block)
    elif lat and lng:
        block_id_list = get_block_id_list_from_lat_lng(user_id, lat, lng, ta2_user_block)
    if add_start_date:
        layer_id_list = get_layer_id_list_by_add_date(user_name, block_id_list, ta1_layer, add_start_date)
    else:
        layer_id_list = get_layer_id_list(block_id_list, ta2_layer, start_date, end_date)
    task_id_list = request_multiband_tasks(user_id, layer_id_list, ta2_task)
    download_url_list = check_tasks_until_finish(task_id_list, ta2_task)
    return download_url_list
def check_tasks_until_finish(task_id_list, ta2_task):
    download_url_list = []
    new_task_id_list = []
    while True:
        for task_id in task_id_list:
            task_info = ta2_task.get_task_info(task_id)
            download_url = get_finished_download_link(task_info)
            if download_url:
                download_url_list.append(download_url)
            else:
                new_task_id_list.append(task_id)
        if not new_task_id_list:
            break
        task_id_list = new_task_id_list
        new_task_id_list = []
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


def request_multiband_tasks(user_id, layer_id_list, ta2_task):
    task_id_list = []
    for layer_id in layer_id_list: 
        task_info = ta2_task.request_geotiff_task(user_id, layer_id, multiband=True)
        if task_info:
            if 'task_id' in task_info:
                task_id_list.append(task_info['task_id'])
    return task_id_list

def get_block_id_list_from_block_name(user_id, block_name, ta2_user_block):
    block_id_list = []
    user_blocks = ta2_user_block.get_user_blocks_from_name(user_id, block_name)
    for user_block in user_blocks:
        # print user_block
        block_id_list.append(user_block['blockId'])
    return block_id_list

def get_block_id_list_from_lat_lng(user_id, lat,lng, ta2_user_block):
    block_id_list = []
    user_blocks = ta2_user_block.get_user_blocks_from_gps(user_id, lat,lng)
    for user_block in user_blocks:
        print user_block
    return block_id_list

def get_layer_id_list_by_add_date(user_name, block_id_list, ta1_layer, add_start_date):
    layer_id_list = []
    for block_id in block_id_list:
        print 'block_id', block_id
        add_start_date
        layers = ta1_layer.get_layers(user_name,'MULTIBAND',block_id, )
        if layers:
            print 'layer_id, epoch, date'
            for layer in layers:
                print layer['ndviLayerId'], layer['layerDateEpoch'], datetime.datetime.fromtimestamp(float(layer['layerDateEpoch'])).strftime('%Y-%m-%d')
                if start_date:
                    start_epoch = int(datetime.datetime.strptime(start_date,"%Y-%m-%d").strftime('%s'))
                    if layer['layerDateEpoch'] < start_epoch:
                        print 'filtered by start_date', start_date
                        continue
                if end_date:
                    end_epoch = int(datetime.datetime.strptime(end_date,"%Y-%m-%d").strftime('%s'))
                    if layer['layerDateEpoch'] > end_epoch:
                        print 'filtered by end_date', end_date
                        continue
                layer_id_list.append(layer['ndviLayerId'])
    return layer_id_list

def get_layer_id_list(block_id_list, ta2_layer, start_date=None, end_date=None):
    layer_id_list = []
    for block_id in block_id_list:
        print 'block_id', block_id
        layers = ta2_layer.get_layers(block_id)
        if layers:
            print 'layer_id, epoch, date'
            for layer in layers:
                print layer['ndviLayerId'], layer['layerDateEpoch'], datetime.datetime.fromtimestamp(float(layer['layerDateEpoch'])).strftime('%Y-%m-%d')
                if start_date:
                    start_epoch = int(datetime.datetime.strptime(start_date,"%Y-%m-%d").strftime('%s'))
                    if layer['layerDateEpoch'] < start_epoch:
                        print 'filtered by start_date', start_date
                        continue
                if end_date:
                    end_epoch = int(datetime.datetime.strptime(end_date,"%Y-%m-%d").strftime('%s'))
                    if layer['layerDateEpoch'] > end_epoch:
                        print 'filtered by end_date', end_date
                        continue
                layer_id_list.append(layer['ndviLayerId'])
    return layer_id_list
