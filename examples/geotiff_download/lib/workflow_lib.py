import os
import json
import time
import logging
import datetime

from lib.product_lib import ProductLib
from lib.cog_raster_lib import CogRasterLib
from lib.api2.ta_user import TerrAvionAPI2User
from lib.api2.ta_block import TerrAvionAPI2Block
from lib.api2.ta_user_block import TerrAvionAPI2UserBlock
from lib.api2.ta_layer import TerrAvionAPI2Layer
from lib.api2.ta_task import TerrAvionAPI2Task
from util.file_util import clean_filename, run_download_file


def date_to_epoch(date_string):
    if date_string:
        epoch_start = datetime.datetime(1970, 1, 1)
        epoch_input = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return int((epoch_input - epoch_start).total_seconds())
    else:
        return None


def validate_product(product):
    log = logging.getLogger(__name__)

    product_list = [
        'MULTIBAND', 'SYNTHETIC_NC', 'SYNTHETIC_COLOR', 'SYNTHETIC_RGB',
        'NC', 'COLOR', 'RGB', 'CIR', 'INFRARED', 'NDVI', 'VIGOR',
        'TIRS', 'THERMAL', 'PANSHARPEN_TIRS', 'PANSHARPEN_THERMAL',
        'ZONE', 'ZONING', 'CANOPY_VIGOR'
    ]

    if product in product_list:
        return True
    else:
        log.error('Please select a valid product: %s', str(product_list))
        return False


def get_cog_multiband_download_links(access_token, block_name=None,
                                     lat=None, lng=None, block_id_list=None,
                                     start_date=None, end_date=None,
                                     add_start_date=None, output_dir=None,
                                     print_summary=False, no_clipping=False,
                                     product=None):
    log = logging.getLogger(__name__)

    if product:
        if validate_product(product) is False:
            return None

    tapi2_block = TerrAvionAPI2Block(access_token)
    ta2_user = TerrAvionAPI2User(access_token)
    user_id = ta2_user.get_user_id()

    ta2_layer = TerrAvionAPI2Layer(
        user_id,
        access_token,
        epoch_start=date_to_epoch(start_date),
        epoch_end=date_to_epoch(end_date),
        add_epoch_start=date_to_epoch(add_start_date))

    layer_info_list = []

    if block_id_list:
        layer_info_list = ta2_layer.get_layers_by_block_id_list(block_id_list)
    else:
        layer_info_list = ta2_layer.get_layers(field_name=block_name)

    if not layer_info_list:
        log.info('No layer found')
        return None

    if print_summary:
        if layer_info_list:
            print_layer_summary(layer_info_list, access_token)
        else:
            log.info('Found 0 layers')
    else:
        for layer_info in layer_info_list:
            log.debug('layer_info: %s', json.dumps(layer_info, indent=2, sort_keys=True))

            block_id = layer_info['blockId']
            block_info = tapi2_block.get_geom(block_id)

            log.debug('block_info: %s', json.dumps(block_info))

            s3_url = layer_info.get('cogUrl', None)

            product_args = {}

            # Add contrast boundaries to product_args
            contrast_bounds = layer_info.get('contrastBounds', None)

            if contrast_bounds:
                if 'NC' in contrast_bounds:
                    if 'lower' in contrast_bounds['NC'] and 'upper' in contrast_bounds['NC']:
                        product_args['nc_lower_bound'] = contrast_bounds['NC']['lower']
                        product_args['nc_upper_bound'] = contrast_bounds['NC']['upper']

                if 'NIR' in contrast_bounds:
                    if 'lower' in contrast_bounds['NIR'] and 'upper' in contrast_bounds['NIR']:
                        product_args['nir_lower_bound'] = contrast_bounds['NIR']['lower']
                        product_args['nir_upper_bound'] = contrast_bounds['NIR']['upper']

            if s3_url:
                root_name, ext = os.path.splitext(os.path.basename(s3_url))
                multiband_filename = root_name + '.tif'

                if not no_clipping:
                    root_name = block_id + '_' + root_name
                    multiband_filename = root_name + '.tif'

                if output_dir:
                    multiband_filename = os.path.join(output_dir, multiband_filename)

                if not os.path.isfile(multiband_filename):
                    CogRasterLib().download_cog_from_s3(
                        s3_url=s3_url,
                        outfile=multiband_filename,
                        epsg=4326,
                        geojson_string=json.dumps(block_info),
                        output_dir=output_dir,
                        no_clipping=no_clipping)

                if multiband_filename and output_dir and product and product != 'MULTIBAND':
                    p_l = ProductLib(
                        product=product,
                        input_filepath=multiband_filename,
                        product_args=product_args,
                        output_dir=output_dir,
                        root_name=root_name)

                    p_l.create_product()


def print_layer_summary(layer_info_list, access_token):
    log = logging.getLogger(__name__)
    tapi2_block = TerrAvionAPI2Block(access_token)

    block_dic = {}
    log.info('found %s layers', str(len(layer_info_list)))

    for layer_info in layer_info_list:
        block_id = layer_info['blockId']

        if block_id in block_dic:
            block_info = block_dic[block_id]
        else:
            block_info = tapi2_block.get_block(block_id)

        log.debug('layer_info: %s', json.dumps(layer_info, indent=2, sort_keys=True))
        log.debug('block_info: %s', json.dumps(block_info, indent=2, sort_keys=True))

        epoch_time = layer_info['layerDateEpoch']
        cog_url = layer_info['cogUrl']

        cog_info = {}
        cog_info['cog_url'] = cog_url
        cog_info['layer_date'] = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d')

        layers = []
        if 'layers' in block_info:
            layers = block_info['layers']

        layers.append(cog_info)
        layers = sorted(layers, key=lambda x: x['layer_date'], reverse=True)

        block_info['layers'] = layers
        block_dic[block_id] = block_info

    for block_id in block_dic:
        log.info(json.dumps(block_dic[block_id], sort_keys=True, indent=2))


def get_download_links(access_token, block_name=None, lat=None, lng=None,
                       block_id_list=None, start_date=None, end_date=None,
                       add_start_date=None, geotiff_epsg=None, product=None,
                       with_colormap=False):
    log = logging.getLogger(__name__)
    log.debug(' '.join([
        str(access_token), str(block_name),
        str(lat), str(lng), str(block_id_list)
    ]))

    ta2_user = TerrAvionAPI2User(access_token)
    user_id = ta2_user.get_user_id()

    ta2_layer = TerrAvionAPI2Layer(
        user_id,
        access_token,
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
        log.debug('No layers found')
        return None

    log.info('%s layers found', str(len(layer_info_list)))
    ta2_task = TerrAvionAPI2Task(user_id, access_token)

    if product:
        task_info_list = request_geotiff_tasks(
            ta2_task, layer_info_list,
            geotiff_epsg, product, with_colormap)

        download_url_list = check_tasks_until_finish(task_info_list, ta2_task)

        return download_url_list

    else:
        for layer_info in layer_info_list:
            if 'layerDateEpoch' in layer_info:
                layer_date = datetime.datetime.utcfromtimestamp(layer_info['layerDateEpoch'])
                layer_date_string = layer_date.strftime("%Y-%m-%d")

                add_date = datetime.datetime.utcfromtimestamp(layer_info['addDateEpoch'])
                add_date_string = add_date.strftime("%Y-%m-%d")

                log.info(json.dumps(layer_info, sort_keys=True, indent=2))
                log.info('layer_date: %s', str(layer_date_string))
                log.info('add_date: %s', str(add_date_string))


def check_tasks_until_finish(task_info_list, ta2_task):
    log = logging.getLogger(__name__)
    download_url_list = []
    new_task_info_list = []

    log.info('%s tasks to be downloaded', str(len(task_info_list)))

    while True:
        if task_info_list:
            log.info('%s tasks remaining', str(len(task_info_list)))

        for task_info in task_info_list:
            task_response = ta2_task.get_task_info(task_info['task_id'])

            # If finished, get download link
            download_url = get_finished_download_link(task_response)

            if download_url is not None:
                task_info['download_url'] = download_url
                download_url_list.append(task_info)
            else:
                new_task_info_list.append(task_info)

        if not new_task_info_list:
            break

        task_info_list = new_task_info_list
        new_task_info_list = []

        # Sleeping for 10 seconds
        log.info('Waiting for tasks to finish, sleeping for 10 seconds...')
        time.sleep(10)

    log.info('%s downloads ready', str(len(download_url_list)))

    return download_url_list


def get_finished_download_link(task_info):
    if not task_info:
        return None

    elif 'status' not in task_info:
        return None

    elif task_info['status'] != 'DONE':
        return None

    elif 'response' not in task_info:
        return None

    elif 'download_url' in task_info['response']:
        return task_info['response']['download_url']

    else:
        return None


def request_geotiff_tasks(ta2_task, layer_info_list, geotiff_epsg=None,
                          product='MULTIBAND', with_colormap=False):
    log = logging.getLogger(__name__)
    task_info_list = []

    for layer_info in layer_info_list:
        if product == 'MULTIBAND' and layer_info['ndviLayerId']:
            layer_id = layer_info['ndviLayerId']

            task_info = ta2_task.request_geotiff_task(
                layer_id, multiband=True, geotiff_epsg=geotiff_epsg)

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

            nc_layer_dict = {'layer_id': layer_info['ncLayerId'], 'product': 'RGB'}
            cir_layer_dict = {'layer_id': layer_info['cirLayerId'], 'product': 'CIR'}
            ndvi_layer_dict = {'layer_id': layer_info['ndviLayerId'], 'product': 'NDVI'}
            thermal_layer_dict = {'layer_id': layer_info['thermalLayerId'], 'product': 'THERMAL'}
            multiband_layer_dict = {'layer_id': layer_info['ndviLayerId'], 'product': 'MULTIBAND'}

            if product == 'FULL':
                product_info_list.append(nc_layer_dict)
                product_info_list.append(cir_layer_dict)

                if layer_info['ndviLayerId']:
                    product_info_list.append(ndvi_layer_dict)

                if layer_info['thermalLayerId']:
                    product_info_list.append(thermal_layer_dict)

            elif product == 'ALL':
                product_info_list.append(nc_layer_dict)
                product_info_list.append(cir_layer_dict)

                if layer_info['ndviLayerId']:
                    product_info_list.append(ndvi_layer_dict)

                if layer_info['thermalLayerId']:
                    product_info_list.append(thermal_layer_dict)

                product_info_list.append(multiband_layer_dict)

            elif product == 'NC':
                product_info_list.append(nc_layer_dict)

            elif product == 'CIR':
                product_info_list.append(cir_layer_dict)

            elif product == 'NDVI':
                if layer_info['ndviLayerId']:
                    product_info_list.append(ndvi_layer_dict)

            elif product == 'TIRS':
                if layer_info['thermalLayerId']:
                    product_info_list.append(thermal_layer_dict)

            for product_info in product_info_list:
                log.debug('product_info: %s', json.dumps(product_info, indent=2, sort_keys=True))

                if not product_info['layer_id']:
                    log.debug('Missing layer_id')
                    continue

                if product_info['product'] == 'MULTIBAND':
                    task_info = ta2_task.request_geotiff_task(
                        product_info['layer_id'],
                        geotiff_epsg=geotiff_epsg,
                        multiband=True)
                else:
                    colormap = None

                    if with_colormap:
                        if product_info['product'] == 'THERMAL':
                            colormap = 'T'
                        elif product_info['product'] == 'NDVI':
                            colormap = 'NDVI_2'

                    task_info = ta2_task.request_geotiff_task(
                        product_info['layer_id'],
                        geotiff_epsg=geotiff_epsg,
                        colormap=colormap)

                task_info['product'] = product_info['product']
                task_info['addDateEpoch'] = add_epoch
                task_info['layerDateEpoch'] = layer_epoch
                task_info['blockId'] = layer_info['blockId']

                if 'task_id' in task_info:
                    task_info_list.append(task_info)

    return task_info_list


def download_imagery(access_token, output_dir, download_info_list):
    log = logging.getLogger(__name__)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    ta_b = TerrAvionAPI2Block(access_token)

    if not download_info_list:
        logging.info('no download links')
        return None

    logging.info('%s files to be downloaded', str(len(download_info_list)))

    unique_names = True
    check_unique_dic = {}
    downloaded_list = []

    for download_info in download_info_list:
        block_info = ta_b.get_block(download_info['blockId'])
        field_name = clean_filename(block_info['name'])

        if field_name not in check_unique_dic:
            check_unique_dic[field_name] = True
        else:
            unique_names = False
            break

    for download_info in download_info_list:
        try:
            logging.debug(json.dumps(download_info, sort_keys=True, indent=2))

            block_info = ta_b.get_block(download_info['blockId'])
            field_name = clean_filename(block_info['name'])
            layer_date = datetime.datetime.utcfromtimestamp(download_info['layerDateEpoch'])
            layer_date_string = layer_date.strftime("%Y-%m-%d")
            root_name = layer_date_string
            root_name += '_' + field_name + '_'

            if not unique_names:
                root_name += download_info['blockId'] + '_'

            root_name += download_info['product'] + '.tif'
            out_file = os.path.join(output_dir, root_name)

            logging.debug('url: %s', str(download_info['download_url']))
            logging.debug('out_file: %s', str(out_file))
            logging.debug(json.dumps(download_info, sort_keys=True, indent=2))

            run_download_file(download_info['download_url'], out_file)
            downloaded_list.append(out_file)

        except:
            log.critical('Download Failed: %s', str(download_info['download_url']))
            log.critical('out_file: %s', str(out_file))

    log.info('Download Complete: %s files downloaded', str(len(downloaded_list)))
