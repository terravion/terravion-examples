import os
import gdal
import argparse
import numpy as np
from os.path import basename

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
    north_south_pix_res = geoT[5]
    ground_resolution_cm = round(latLon2Meters(
        lat, lng, lat + west_east_pix_res, lng) * 1000 * 100, 2)
    return ground_resolution_cm
def latLon2Meters(lat1, lon1, lat2, lon2):
    '''
    http://en.wikipedia.org/wiki/Great-circle_distance
    http://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
    function measure(lat1, lon1, lat2, lon2){ // generally used geo measurement function
    var R = 6378.137; // Radius of earth in KM
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLon = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;
    return d * 1000; // meters
    }
    '''

    R = 6378.137
    dLat = (lat2 - lat1) * np.pi / 180.0
    dLon = (lon2 - lon1) * np.pi / 180.0
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(lat1 * np.pi / 180) * \
    np.cos(lat2 * np.pi / 180) * np.sin(dLon / 2) * np.sin(dLon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c

    return d

if __name__ == '__main__':
    argument_sample = 'python ' + basename(os.path.realpath(__file__)) + \
        ' -input_file <input_file>'

    parser = argparse.ArgumentParser(description=argument_sample)

    parser.add_argument('-input_file', help='input_file',
                        nargs='?', default=None)
    args = parser.parse_args()
    main(args)