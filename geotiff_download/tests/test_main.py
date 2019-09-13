import os
import json
import logging
from . import root_env
import tests.config as config
from lib.api2.ta_user import TerrAvionAPI2User
from lib.api2.ta_user_block import TerrAvionAPI2UserBlock
from lib.workflow_lib import get_download_links, download_imagery

logging.basicConfig(level=logging.INFO)


class TestMain(object):
    def test_get_block_list(self):
        log = logging.getLogger(__name__)
        access_token = config.ACCESS_TOKEN

        ta2_user = TerrAvionAPI2User(access_token)
        user_id = ta2_user.get_user_id()

        ta2_user_block = TerrAvionAPI2UserBlock(user_id, access_token)
        user_block_list = ta2_user_block.get_user_blocks()

        log.info('block_id, name')

        for user_block in user_block_list:
            log.info(','.join([user_block['blockId'], user_block['fieldName']]))

        assert True

    def test_start_end_date(self):
        log = logging.getLogger(__name__)
        access_token = config.ACCESS_TOKEN

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        working_dir = os.path.join(root_dir, 'download')

        block_name = None
        lat = None
        lng = None
        block_id_list = ['82f9ecc1-7b29-440a-87fc-3dd8b47e400c']
        start_date = '2017-10-23'
        end_date = '2017-10-30'
        add_start_date = None
        geotiff_epsg = None
        product = 'ALL'
        with_colormap = False

        download_info_list = get_download_links(
            access_token, block_name, lat, lng, block_id_list,
            start_date, end_date, add_start_date, geotiff_epsg,
            product=product, with_colormap=with_colormap)

        if download_info_list:
            if working_dir:
                download_imagery(access_token, working_dir, download_info_list)
            else:
                for download_info in download_info_list:
                    log.debug(json.dumps(download_info, sort_keys=True, indent=2))

        assert True

    def test_add_date(self):
        log = logging.getLogger(__name__)
        access_token = config.ACCESS_TOKEN

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        working_dir = os.path.join(root_dir, 'download')

        block_name = None
        lat = None
        lng = None
        block_id_list = ['c0dac568-f49d-4d9f-a1d5-20f32bb0d402']
        start_date = None
        end_date = None
        add_start_date = '2017-11-20'
        geotiff_epsg = None
        product = 'ALL'
        with_colormap = True

        download_info_list = get_download_links(
            access_token, block_name, lat, lng, block_id_list,
            start_date, end_date, add_start_date, geotiff_epsg,
            product=product, with_colormap=with_colormap)

        if download_info_list:
            if working_dir:
                download_imagery(access_token, working_dir, download_info_list)
            else:
                for download_info in download_info_list:
                    log.debug(json.dumps(download_info, sort_keys=True, indent=2))

        return True
