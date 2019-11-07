import os
import gdal
import argparse
import numpy as np


def main(args):
    # Input Parameter
    input_file = args.input_file

    if input_file:
        ground_resolution_cm = analyze_tif_cm_4326(input_file)
        print('ground_resolution_cm', ground_resolution_cm)
    else:
        print('--------------------------------------------------------------------------------------------------------------------------------')
        print(parser.print_help())
        print('--------------------------------------------------------------------------------------------------------------------------------')


def analyze_tif_cm_4326(input_file):
    src = gdal.Open(input_file, gdal.GA_ReadOnly)
    geoT = src.GetGeoTransform()
    # GeoTransform[0] /* upper left x */
    # GeoTransform[1] /* west-east pixel resolution */
    # GeoTransform[2] /* 0 */
    # GeoTransform[3] /* upper left y */
    # GeoTransform[4] /* 0 */
    # GeoTransform[5] /* north-south pixel resolution (negative value) */

    lat = geoT[0]
    lng = geoT[3]
    west_east_pix_res = geoT[1]
    # north_south_pix_res = geoT[5]

    ground_resolution_cm = round(lat_lon_2_meters(
        lat, lng, lat + west_east_pix_res, lng) * 100, 2)

    return ground_resolution_cm


def lat_lon_2_meters(self, lat1, lon1, lat2, lon2):
    return haversine(lat1, lon1, lat2, lon2)


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2) ** 2 + \
        np.cos(lat1) * np.cos(lat2) * \
        np.sin(dlon / 2) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    R = 6378137.0  # Radius of earth in meters. Use 3956 for miles

    return R * c


if __name__ == '__main__':
    argument_sample = 'python ' + os.path.basename(os.path.realpath(__file__)) + \
        ' -input_file <input_file>'

    parser = argparse.ArgumentParser(description=argument_sample)

    parser.add_argument('-input_file', help='input_file',
                        nargs='?', default=None)
    args = parser.parse_args()
    main(args)
