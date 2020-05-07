import os
import rasterio
import json
import logging
import numpy as np
import skimage
from skimage.filters.rank import median
from skimage.morphology import disk


from util.image_tools import (
    rescale_intensity_to_bounds,
    convert_16bit_to_8bit,
    clean_zeros_with_mask,
    pansharpen,
    UINT8,
    UINT16
)

from lib.cog_raster_lib import CogRasterLib


class ProductLib(object):
    def __init__(self, product, contrast_bounds=None, input_filepath=None,
                 product_args=None, output_dir=None, root_name=None):
        self.log = logging.getLogger(__name__)
        self.product = product.upper()
        self.output_dir = output_dir
        self.root_name = root_name
        self.input_filepath = input_filepath
        self.cog_tags = CogRasterLib().get_cog_tags(input_filepath)
        self.block_size = 10

        self.product_args = {
            'ndvi_alpha': 0.0,
            'ndvi_beta': 1.0,
            'ndvi_low': 0.0,
            'ndvi_high': 1.0,
            'lowdegc': 0,
            'highdegc': 70,
            'si_unit': 'decikelvin',
            'singleband': False,
            'colormap': None
        }

        # NOTE: For backwards compatability with previous version 1.0.0
        # contrast_bounds input will be deprecated in next major version
        if contrast_bounds is not None:
            self.handle_contrast_bounds_input(contrast_bounds)

        # Overwrite global args with user input
        # NOTE: Overwrites values if dictionary is not empty or None
        if product_args and isinstance(product_args, dict):
            for key, value in product_args.items():
                self.product_args[key] = value

    def create_product(self, out_filepath=None):
        if not out_filepath and self.output_dir and self.root_name:
            out_filepath = os.path.join(
                self.output_dir,
                self.root_name + '_' + self.product + '.tif')

        if self.product in ['SYNTHETIC_NC', 'SYNTHETIC_COLOR', 'SYNTHETIC_RGB']:
            self.make_synthetic_nc(out_filepath)

        elif self.product in ['NC', 'COLOR', 'RGB']:
            self.make_nc(out_filepath)

        elif self.product in ['CIR', 'INFRARED']:
            self.make_cir(out_filepath)

        elif self.product in ['NDVI', 'VIGOR']:
            self.make_ndvi(out_filepath)

        elif self.product in ['ZONE', 'ZONING', 'CANOPY_VIGOR']:
            self.make_zone(out_filepath)

        elif self.product in ['TIRS', 'THERMAL']:
            self.make_tirs(out_filepath)

        elif self.product in ['PANSHARPEN_TIRS', 'PANSHARPEN_THERMAL']:
            self.make_pansharpen_tirs(out_filepath)

        else:
            self.log.error('Invalid product type: %s', str(self.product))

    def make_synthetic_nc(self, output_filepath):
        self.log.info('Creating synthetic NC product')

        with rasterio.open(self.input_filepath) as src:
            B, G, R = map(src.read, (1, 2, 3))
            B2, G2, R2 = map(src.read, (4, 5, 6))
            kwargs = src.meta

        mask = (R == 0)

        B = np.asarray(B, dtype=np.float)
        G = np.asarray(G, dtype=np.float)
        R = np.asarray(R, dtype=np.float)

        B2 = np.asarray(B2, dtype=np.float)
        G2 = np.asarray(G2, dtype=np.float)
        R2 = np.asarray(R2, dtype=np.float)

        pan = 0.3 * R2 + 0.59 * G2 + 0.11 * R2

        del R2, G2, B2

        R, G, B = pansharpen(R, G, B, pan, method='browley', W=0.25)

        del pan

        R = np.asarray(R, dtype=np.uint16)
        G = np.asarray(G, dtype=np.uint16)
        B = np.asarray(B, dtype=np.uint16)

        lower = self.product_args.get('nir_lower_bound', None)
        upper = self.product_args.get('nir_upper_bound', None)

        if lower and upper:
            R = rescale_intensity_to_bounds(R, lower, upper)
            G = rescale_intensity_to_bounds(G, lower, upper)
            B = rescale_intensity_to_bounds(B, lower, upper)
        else:
            R = np.multiply(R, 20.0)
            G = np.multiply(G, 20.0)
            B = np.multiply(B, 20.0)

        R = convert_16bit_to_8bit(R)
        G = convert_16bit_to_8bit(G)
        B = convert_16bit_to_8bit(B)

        # Fixes nodata holes in middle of data caused by rescaling
        R = clean_zeros_with_mask(R, mask)
        G = clean_zeros_with_mask(G, mask)
        B = clean_zeros_with_mask(B, mask)

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(R, 1)
            dst.write(G, 2)
            dst.write(B, 3)
            dst.nodata = 0

    def make_nc(self, output_filepath):
        self.log.info('Creating NC product')

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            R, G, B = map(src.read, (3, 2, 1))
            kwargs = src.meta

        lower = self.product_args.get('nc_lower_bound', None)
        upper = self.product_args.get('nc_upper_bound', None)

        mask = (R == 0)

        if lower and upper:
            R = rescale_intensity_to_bounds(R, lower, upper)
            G = rescale_intensity_to_bounds(G, lower, upper)
            B = rescale_intensity_to_bounds(B, lower, upper)
        else:
            R = np.multiply(R, 20.0)
            G = np.multiply(G, 20.0)
            B = np.multiply(B, 20.0)

        R = convert_16bit_to_8bit(R)
        G = convert_16bit_to_8bit(G)
        B = convert_16bit_to_8bit(B)

        # Fixes nodata holes in middle of data caused by rescaling
        R = clean_zeros_with_mask(R, mask)
        G = clean_zeros_with_mask(G, mask)
        B = clean_zeros_with_mask(B, mask)

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(R, 1)
            dst.write(G, 2)
            dst.write(B, 3)
            dst.nodata = 0

    def make_cir(self, output_filepath):
        self.log.info('Creating CIR product')

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            R, G, B = map(src.read, (4, 6, 5))
            kwargs = src.meta

        lower = self.product_args.get('nir_lower_bound', None)
        upper = self.product_args.get('nir_upper_bound', None)

        mask = (R == 0)

        if lower and upper:
            R = rescale_intensity_to_bounds(R, lower, upper)
            G = rescale_intensity_to_bounds(G, lower, upper)
            B = rescale_intensity_to_bounds(B, lower, upper)
        else:
            R = np.multiply(R, 10.0)
            G = np.multiply(G, 10.0)
            B = np.multiply(B, 10.0)

        R = convert_16bit_to_8bit(R)
        G = convert_16bit_to_8bit(G)
        B = convert_16bit_to_8bit(B)

        # Fixes nodata holes in middle of data caused by rescaling
        R = clean_zeros_with_mask(R, mask)
        G = clean_zeros_with_mask(G, mask)
        B = clean_zeros_with_mask(B, mask)

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(R, 1)
            dst.write(G, 2)
            dst.write(B, 3)
            dst.nodata = 0

    def make_ndvi(self, output_filepath):
        self.log.info('Creating NDVI product')

        sndvi_beta = self.product_args['ndvi_beta']
        sndvi_alpha = self.product_args['ndvi_alpha']
        low = self.product_args['ndvi_low']
        high = self.product_args['ndvi_high']
        singleband = self.product_args['singleband']
        colormap = self.product_args['colormap']

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            NIR, RED = map(src.read, (4, 6))
            tags_dict = dict(src.tags())

            if 'NDVI_BETA' in tags_dict and 'NDVI_ALPHA' in tags_dict:
                sndvi_beta = float(tags_dict['NDVI_BETA'])
                sndvi_alpha = float(tags_dict['NDVI_ALPHA'])

            kwargs = src.meta

        mask = (RED == 0)

        ndvi = self.calculate_ndvi(RED, NIR,
                                   alpha=sndvi_alpha,
                                   beta=sndvi_beta,
                                   low=low, high=high)
        ndvi *= UINT8

        self.log.debug('Clipping data to 8bit as a precaution')
        ndvi = np.clip(ndvi, 0, UINT8).astype(np.uint8)

        self.log.debug('NDVI mean: %s', str(np.mean(ndvi)))
        self.log.debug('NDVI std: %s', str(np.std(ndvi)))

        # Fixes nodata holes in middle of data caused by rescaling
        ndvi = clean_zeros_with_mask(ndvi, mask)

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        if colormap:
            singleband = True

        if singleband:
            kwargs.update(alpha='no', count=1)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(ndvi, 1)

            if not singleband:
                dst.write(ndvi, 2)
                dst.write(ndvi, 3)

            if colormap:
                dst.write_colormap(1, colormap)

            dst.nodata = 0

    def make_zone(self, output_filepath):
        self.log.info('Creating ZONE product')

        sndvi_beta = self.product_args['ndvi_beta']
        sndvi_alpha = self.product_args['ndvi_alpha']
        low = self.product_args['ndvi_low']
        high = self.product_args['ndvi_high']
        singleband = self.product_args['singleband']
        colormap = self.product_args['colormap']

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            NIR, RED = map(src.read, (4, 6))
            tags_dict = dict(src.tags())

            if 'NDVI_BETA' in tags_dict and 'NDVI_ALPHA' in tags_dict:
                sndvi_beta = float(tags_dict['NDVI_BETA'])
                sndvi_alpha = float(tags_dict['NDVI_ALPHA'])

            kwargs = src.meta

        ndvi = self.calculate_ndvi(RED, NIR,
                                   alpha=sndvi_alpha,
                                   beta=sndvi_beta,
                                   low=low, high=high)

        threshold = 0.2

        ndvi[np.where(ndvi < threshold)] = 0
        ndvi_8bit = np.clip(ndvi * UINT8, 0, UINT8)
        ndvi_processed = median(ndvi, disk(self.block_size),
                                mask=(ndvi_8bit > threshold * UINT8))

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        if colormap:
            singleband = True

        if singleband:
            kwargs.update(alpha='no', count=1)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(ndvi_processed, 1)

            if not singleband:
                dst.write(ndvi_processed, 2)
                dst.write(ndvi_processed, 3)

            if colormap:
                dst.write_colormap(1, colormap)

            dst.nodata = 0

    def make_tirs(self, output_filepath):
        self.log.info('Creating TIRS product')

        lowdegc = self.product_args['lowdegc']
        highdegc = self.product_args['highdegc']
        si_unit = self.product_args['si_unit']
        singleband = self.product_args['singleband']
        colormap = self.product_args['colormap']

        # Get the red and NIR bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            t = src.read(7)
            thermal_tags = src.tags(7)
            kwargs = src.meta

        old_thermal_flag = False

        if 'SI_UNIT' in thermal_tags:
            if thermal_tags['SI_UNIT'] == 'decikelvin':
                old_thermal_flag = True
        else:
            old_thermal_flag = True

        # Override onboard tiff tags if si_unit given in product_args
        if si_unit == 'centikelvin':
            old_thermal_flag = False

        # temp_range_max = 0.04 * UINT8

        t = np.asarray(t, dtype=np.float)

        if old_thermal_flag is True:
            t = np.divide(t, 10.0)
        else:
            t = np.divide(t, 100.0)

        low = lowdegc + 273.15
        high = highdegc + 273.15

        self.log.debug('TIRS low temp bound celcius:  %s', str(lowdegc))
        self.log.debug('TIRS high temp bound celcius: %s', str(highdegc))
        self.log.debug('TIRS low temp bound scaled:   %s', str(low))
        self.log.debug('TIRS high temp bound scaled:  %s', str(high))

        if np.count_nonzero(t) > 0:
            max_t = np.max(t)
            min_t = np.min(t[np.nonzero(t)])

            self.log.debug('Max (C/K): %s / %s', str(max_t - 273.15), str(max_t))
            self.log.debug('Min (C/K): %s / %s', str(min_t - 273.15), str(min_t))

        # middle_value = (np.max(t) + np.min(t)) / 2.0
        # # middle_value = np.max(t) - temp_range_max / 2.0
        # # middle_value = np.min(t) + temp_range_max / 2.0

        # low = middle_value - temp_range_max / 2.0
        # high = middle_value + temp_range_max / 2.0

        # print 'Temp Range Max:', temp_range_max
        # print 'Middle (C/K):', middle_value - 273.15, '/', middle_value
        # print 'Low (C/K):', low - 273.15, '/', low
        # print 'High (C/K):', high - 273.15, '/', high

        # Scale thermal values to low / high values
        t = (t - low) / (high - low)

        # Clip to make sure we're within the range
        t = np.multiply(t, UINT8)
        t = np.asarray(t, dtype=np.uint8)
        t = np.clip(t, 0, UINT8).astype(np.uint8)

        # Now write the bands in the standard RGB
        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        if colormap:
            singleband = True

        if singleband:
            kwargs.update(alpha='no', count=1)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(t, 1)

            if not singleband:
                dst.write(t, 2)
                dst.write(t, 3)

            if colormap:
                dst.write_colormap(1, colormap)

            dst.nodata = 0

    def make_pansharpen_tirs(self, output_filepath):
        self.log.info('Creating pansharpen TIRS product')

        lowdegc = self.product_args['lowdegc']
        highdegc = self.product_args['highdegc']
        si_unit = self.product_args['si_unit']
        singleband = self.product_args['singleband']
        colormap = self.product_args['colormap']

        with rasterio.open(self.input_filepath) as src:
            B, G, R, t = map(src.read, (4, 5, 6, 7))
            thermal_tags = src.tags(7)
            kwargs = src.meta

        old_thermal_flag = False

        if 'SI_UNIT' in thermal_tags:
            if thermal_tags['SI_UNIT'] == 'decikelvin':
                old_thermal_flag = True
        else:
            old_thermal_flag = True

        # Override onboard tiff tags if si_unit given in product_args
        if si_unit == 'centikelvin':
            old_thermal_flag = False

        mask = (R == 0)

        # temp_range_max = 0.04 * UINT8

        t = np.asarray(t, dtype=np.float)

        if old_thermal_flag is True:
            t = np.divide(t, 10.0)
        else:
            t = np.divide(t, 100.0)

        low = lowdegc + 273.15
        high = highdegc + 273.15

        t = (t - low) / (high - low)

        # Scale to 16-bit
        t = np.multiply(t, UINT16)

        R = np.asarray(R, dtype=np.float)
        G = np.asarray(G, dtype=np.float)
        B = np.asarray(B, dtype=np.float)

        gray = 0.3 * R + 0.59 * G + 0.11 * B

        gray = np.asarray(gray, dtype=np.float)

        t -= gray * 1.6
        t *= 1.3

        pan = convert_16bit_to_8bit(t)

        # Fixes nodata holes in middle of data caused by rescaling
        pan = clean_zeros_with_mask(pan, mask)

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        kwargs.update(alpha='no', count=3)

        if colormap:
            singleband = True

        if singleband:
            kwargs.update(alpha='no', count=1)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(pan, 1)

            if not singleband:
                dst.write(pan, 2)
                dst.write(pan, 3)

            if colormap:
                dst.write_colormap(1, colormap)

            dst.nodata = 0

    def calculate_ndvi(self, red, nir, alpha=0.0, beta=1.0, low=0.0, high=1.0):
        red = np.asarray(red, dtype=np.float32)
        nir = np.asarray(nir, dtype=np.float32)

        ndvi = np.divide(nir - red, nir + red)
        ndvi[np.isnan(ndvi)] = 0
        ndvi[np.isinf(ndvi)] = 0

        if alpha != 0.0:
            ndvi += alpha

        if beta != 1.0:
            ndvi *= beta

        # Ignore calculation if values will not change result
        if low != 0.0 and high != 1.0:
            ndvi = (ndvi - low) / (high - low)

        self.log.debug('NDVI min/max: %s / %s', str(np.min(ndvi)), str(np.max(ndvi)))
        self.log.debug('99th percentile: %s', str(np.percentile(ndvi, 99)))
        self.log.debug('1st percentile: %s', str(np.percentile(ndvi, 1)))

        ndvi[np.isnan(ndvi)] = 0
        ndvi[np.isinf(ndvi)] = 0
        ndvi[ndvi < 0] = 0

        return ndvi

    def handle_contrast_bounds_input(self, contrast_bounds):
        # NOTE: Will be deprecated soon
        if 'NC' in contrast_bounds:
            if 'lower' in contrast_bounds['NC'] and 'upper' in contrast_bounds['NC']:
                self.product_args['nc_lower_bound'] = contrast_bounds['NC']['lower']
                self.product_args['nc_upper_bound'] = contrast_bounds['NC']['upper']

        if 'NIR' in contrast_bounds:
            if 'lower' in contrast_bounds['NIR'] and 'upper' in contrast_bounds['NIR']:
                self.product_args['nir_lower_bound'] = contrast_bounds['NIR']['lower']
                self.product_args['nir_upper_bound'] = contrast_bounds['NIR']['upper']
