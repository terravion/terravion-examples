
import numpy as np
import skimage

UINT8 = float(2**8 - 1)  # 255.0
UINT16 = float(2**16 - 1)  # 65535.0


def convert_16bit_to_8bit(array):
    array = np.clip(array, 0, UINT16).astype(np.uint16)
    array = np.asarray(array, dtype=np.float)
    array = np.divide(array, UINT16)
    array = np.multiply(array, UINT8)
    array = np.asarray(array, dtype=np.uint8)
    array = np.clip(array, 0, UINT8).astype(np.uint8)
    return array


def rescale_intensity_to_bounds(band, lower_bound, upper_bound):
    band = skimage.exposure.rescale_intensity(band, in_range=(lower_bound,
                                                              upper_bound))
    # band = skimage.exposure.adjust_sigmoid(band, cutoff=0.5, gain=5)
    return band


def pansharpen(r, g, b, pan, method='browley', W=0.1):
    rgb = np.empty((r.shape[0], r.shape[1], 3))
    rgb[:, :, 0] = r
    rgb[:, :, 1] = g
    rgb[:, :, 2] = b

    if method == 'simple_browley':
        all_in = r + g + b
        # prod = np.multiply(all_in, pan)

        r = np.multiply(r, pan / all_in)
        g = np.multiply(g, pan / all_in)
        b = np.multiply(b, pan / all_in)

    if method == 'sample_mean':
        r = 0.5 * (r + pan)
        g = 0.5 * (g + pan)
        b = 0.5 * (b + pan)

    if method == 'esri':
        ADJ = pan - rgb.mean(axis=2)
        r = (r + ADJ)
        g = (g + ADJ)
        b = (b + ADJ)

    if method == 'browley':
        pan /= (W * r + W * g + W * b)

        # Multiply by DNF
        r *= pan
        g *= pan
        b *= pan

    return r, g, b
