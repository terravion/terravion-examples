##########################################################################
# TerrAvion Cog Raster Lib
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
import traceback
import rasterio
import json
import logging
import platform
from os.path import basename
if platform.system() == 'Darwin':
    os.environ['CURL_CA_BUNDLE'] = '/usr/local/etc/openssl/cert.pem'
elif platform.system() == 'Windows':
    print('Specific CURL_CA_BUNDLE HERE')
else:
    os.environ['CURL_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'

class CogRasterLib(object):
    def __init__(self):
        self.log = logging.getLogger(__name__)
    def download_cog_from_s3(self, s3_url, outfile, epsg=4326, geojson_file=None, geojson_string=None, working_dir=None, no_clipping=False):
        # Download Multiband from COG
        gdalwarp_cmd_list = [
            'gdalwarp',
            '--config GDAL_CACHEMAX 500',
            '-wm 500',
            '-co BIGTIFF=YES',
            '--config GDALWARP_IGNORE_BAD_CUTLINE YES',
            '-t_srs EPSG:'+ str(epsg),
            '-of GTiff',
        ]
        if not no_clipping:
            gdalwarp_cmd_list.append('-crop_to_cutline -cutline')
            if geojson_file:
                gdalwarp_cmd_list.append(geojson_file)
            elif geojson_string:
                gdalwarp_cmd_list.append("'"+ geojson_string+ "'")
            else:
                raise Exception('Need to supply geojson_file, geojson_string')
        gdalwarp_cmd_list += [
            '/vsicurl/'+ s3_url.replace('s3://', 'https://s3-us-west-2.amazonaws.com/'),
            outfile
        ]

        gdalwarp_cmd = ' '.join(gdalwarp_cmd_list)
        if working_dir:
            self.log.debug(str(gdalwarp_cmd))
            os.system(gdalwarp_cmd)
        else:
            self.log.info('cmd: %s', str(gdalwarp_cmd))
    def validate_terravion_cog(self, file_path):
        '''
            Checking whether it is valid terravion cog geotiff
            file_path could be s3 url or local file path
        '''
        try:
            src = rasterio.open(file_path)
            self.log.debug('src.meta: %s', str(src.meta))
            tags = src.tags()
            self.log.debug('tags: %s', str(tags))
            if not src.meta['count'] == 7:
                return False
            if not 'NDVI_BETA' in tags or not 'NDVI_ALPHA' in tags:
                return False
            for tag_index in range(1, 8):
                band_tag = src.tags(tag_index)
                if not band_tag:
                    return False
                else:
                    self.log.debug('tags[%s]: %s', str(tag_index), str(band_tag))
            return True
        except:
            tb = traceback.format_exc()
            self.log.info('failed: %s', str(tb))
            return False


    def get_cog_tags(self, file_path):
        cog_tags = {}
        with rasterio.open(file_path) as src:
            tags_dict = dict(src.tags())

            if 'NDVI_BETA' in tags_dict and 'NDVI_ALPHA' in tags_dict:
                cog_tags['ndvi_beta'] = float(tags_dict['NDVI_BETA'])
                cog_tags['ndvi_alpha'] = float(tags_dict['NDVI_ALPHA'])

            if src.count == 7:
                thermal_tags = dict(src.tags(7))
                if 'SI_UNIT' in thermal_tags:
                    cog_tags['si_unit'] = thermal_tags['SI_UNIT']
                else:
                    cog_tags['si_unit'] = 'decikelvin'
        return cog_tags