import os
import rasterio
import json
import logging
import numpy as np

from util.image_tools import (
    rescale_intensity_to_bounds,
    convert_16bit_to_8bit,
    pansharpen,
    UINT8
)

from lib.cog_raster_lib import CogRasterLib


class ProductLib(object):
    def __init__(self, product, contrast_bounds, input_filepath, output_dir=None, root_name=None):
        self.log = logging.getLogger(__name__)
        self.product = product
        self.contrast_bounds = contrast_bounds
        self.output_dir = output_dir
        self.root_name = root_name
        self.input_filepath = input_filepath
        self.cog_tags = CogRasterLib().get_cog_tags(input_filepath)

    def create_product(self, out_filepath=None):
        if not out_filepath and self.output_dir and self.root_name:
            out_filepath = os.path.join(
                self.output_dir,
                self.root_name + '_' + self.product + '.tif')

        if self.product == 'SYNTHETIC_NC':
            self.make_synthetic_nc(out_filepath)

        elif self.product == 'NC':
            self.make_nc(out_filepath)

        elif self.product == 'CIR':
            self.make_cir(out_filepath)

        elif self.product == 'TIRS' or self.product == 'THERMAL':
            self.make_thermal(out_filepath)

        elif self.product == 'NDVI':
            self.make_ndvi(out_filepath)

    def make_nc(self, output_filepath):
        self.log.info('Creating NC product')

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            R, G, B = map(src.read, (3, 2, 1))
            band_count = src.count

            if band_count == 8:
                A = src.read(8)

            kwargs = src.meta

        if 'NC' in self.contrast_bounds and 'lower' in self.contrast_bounds['NC'] and 'upper' in self.contrast_bounds['NC']:
            lower = self.contrast_bounds['NC']['lower']
            upper = self.contrast_bounds['NC']['upper']

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

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')

        if band_count == 8:
            A = convert_16bit_to_8bit(A)
            kwargs.update(alpha='yes', count=4)
        else:
            kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(R, 1)
            dst.write(G, 2)
            dst.write(B, 3)

            if band_count == 8:
                dst.write(A, 4)

    def make_cir(self, output_filepath):
        self.log.info('Creating CIR product')

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            R, G, B = map(src.read, (4, 6, 5))

            band_count = src.count

            if band_count == 8:
                A = src.read(8)

            kwargs = src.meta

        if 'NIR' in self.contrast_bounds and 'lower' in self.contrast_bounds['NIR'] and 'upper' in self.contrast_bounds['NIR']:
            lower = self.contrast_bounds['NIR']['lower']
            upper = self.contrast_bounds['NIR']['upper']

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

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')

        if band_count == 8:
            A = convert_16bit_to_8bit(A)
            kwargs.update(alpha='yes', count=4)
        else:
            kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(R, 1)
            dst.write(G, 2)
            dst.write(B, 3)

            if band_count == 8:
                dst.write(A, 4)

    def make_thermal(self, output_filepath):
        self.log.info('Creating TIRS product')

        lowdegc = 0  # 0c
        highdegc = 70  # 70c

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

        t = (t - low) / (high - low)

        # Clip to make sure we're within the range
        t = np.multiply(t, UINT8)
        t = np.asarray(t, dtype=np.uint8)
        t = np.clip(t, 0, UINT8).astype(np.uint8)

        # Update to only have 1 88888888-bit bands,
        # no compression and a colormap

        kwargs.update(dtype=np.uint8, count=1,
                      compress='LZW', alpha='yes')

        # TODO the logic here is funky applying color map and converting back to 3 band. With COG this will go away.
        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(t, 1)

    def make_ndvi(self, output_filepath):
        self.log.info('Creating NDVI product')

        # Get the bands - TA stand geotiff goes B G R N T
        with rasterio.open(self.input_filepath) as src:
            NIR, RED = map(src.read, (4, 6))
            band_count = src.count
            tags_dict = dict(src.tags())

            if 'NDVI_BETA' in tags_dict and 'NDVI_ALPHA' in tags_dict:
                sndvi_beta = float(tags_dict['NDVI_BETA'])
                sndvi_alpha = float(tags_dict['NDVI_ALPHA'])

            if band_count == 8:
                A = src.read(8)

            kwargs = src.meta

        ndvi = self.calculate_ndvi(RED, NIR,
                                   alpha=sndvi_alpha,
                                   beta=sndvi_beta,
                                   low=0, high=1.0)
        ndvi *= UINT8

        self.log.debug('Clipping data to 8bit as a precaution')
        ndvi = np.clip(ndvi, 0, UINT8).astype(np.uint8)

        self.log.debug('NDVI mean: %s', str(np.mean(ndvi)))
        self.log.debug('NDVI std: %s', str(np.std(ndvi)))

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')

        if band_count == 8:
            A = convert_16bit_to_8bit(A)
            kwargs.update(alpha='yes', count=4)
        else:
            kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(output_filepath))

        with rasterio.open(output_filepath, 'w', **kwargs) as dst:
            dst.write(ndvi, 1)
            dst.write(ndvi, 2)
            dst.write(ndvi, 3)

            if band_count == 8:
                dst.write(A, 4)

    def make_synthetic_nc(self, out_filepath):
        self.log.info('Creating synthetic NC product')

        with rasterio.open(self.input_filepath) as src:
            B, G, R = map(src.read, (1, 2, 3))
            B2, G2, R2 = map(src.read, (4, 5, 6))

            band_count = src.count

            if band_count == 8:
                A = src.read(8)

            kwargs = src.meta

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

        if 'NIR' in self.contrast_bounds and 'lower' in self.contrast_bounds['NIR'] and 'upper' in self.contrast_bounds['NIR']:
            lower = self.contrast_bounds['NIR']['lower']
            upper = self.contrast_bounds['NIR']['upper']

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

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')

        if band_count == 8:
            A = convert_16bit_to_8bit(A)
            kwargs.update(alpha='yes', count=4)
        else:
            kwargs.update(alpha='no', count=3)

        self.log.info('Writing file: %s', str(out_filepath))

        with rasterio.open(out_filepath, 'w', **kwargs) as dst:
            dst.write(R, 1)
            dst.write(G, 2)
            dst.write(B, 3)

            if band_count == 8:
                dst.write(A, 4)

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
