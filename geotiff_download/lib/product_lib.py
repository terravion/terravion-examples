import os
import rasterio
import json
import logging
import numpy as np
import util.image_tools as image_tools
class ProductLib(object):
    def __init__(self, product, contrast_bounds, input_filepath, working_dir=None, root_name=None):
        self.log = logging.getLogger(__name__)
        self.product = product
        self.contrast_bounds = contrast_bounds
        self.working_dir = working_dir
        self.root_name = root_name
        self.input_filepath = input_filepath
    def create_product(self, out_filepath):
        if not out_filepath and self.working_dir and self.root_name:
            out_filepath = os.path.join(self.working_dir, self.root_name + '_' + self.product + '.tif')
        if self.product == '':
            self.make_synthetic_nc(out_filepath)

    def make_synthetic_nc(self, output_filepath):
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

        R, G, B = image_tools.pansharpen(R, G, B, pan, method='browley', W=0.65)

        del pan

        R = np.asarray(R, dtype=np.uint16)
        G = np.asarray(G, dtype=np.uint16)
        B = np.asarray(B, dtype=np.uint16)

        if 'NC' in self.contrast_bounds and 'lower' in self.contrast_bounds['NC'] and 'upper' in self.contrast_bounds['NC']:
            lower = self.contrast_bounds['NC']['lower']
            upper = self.contrast_bounds['NC']['upper']

            R = image_tools.rescale_intensity_to_bounds(R, lower, upper)
            G = image_tools.rescale_intensity_to_bounds(G, lower, upper)
            B = image_tools.rescale_intensity_to_bounds(B, lower, upper)
        else:
            R = np.multiply(R, 20.0)
            G = np.multiply(G, 20.0)
            B = np.multiply(B, 20.0)

        R = image_tools.convert_16bit_to_8bit(R)
        G = image_tools.convert_16bit_to_8bit(G)
        B = image_tools.convert_16bit_to_8bit(B)

        kwargs.update(dtype=np.uint8, compress='LZW', photometric='rgb')
        
        if band_count == 8:
            A = image_tools.convert_16bit_to_8bit(A)
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
