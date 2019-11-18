################################################################################
# TerrAvion Color Map Sample
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
# (C) Copyright TerrAvion Inc. 2016
# All rights reserved.
#
#
# AUTHOR
# ------
# William Maio
# wmaio@terravion.com
# http://www.terravion.com
#
################################################################################
import os
import sys
import urllib
from urllib2 import Request, urlopen, URLError, HTTPError

# Contact api@terravion.com for access_token
# default Colormap => N-R3

'''
  "N-AVHRR": "AVHRR",
  "N": "Historic",
  "N-R2": "Wide Range",
  "N-R3": "Default",
  "N-GREENG": "Green Gradient",
  "BW": "Westbrook",
  "GM-RGB3": "GM RGB3",
  "GM-QUAD": "GM QUAD",
  "JG": "JG 0.5 Step Rainbow Palette",
  "GM-COMP1": "GM Complete Range",
  "GRANULAR": "Granular",
  "RW-LEGACY": "RW Legacy",
  "GRANULAR": "Granular",
  "SMWE": "SMWE",
  "CHS-LEGACY": "CHS Legacy",
  "TRICOLOR": "Tricolor",
'''


def main(argv):
    output_dir = argv[0]
    # user_id = 'support+demo@terravion.com'
    access_token = '2e68cee0-b2fd-4ef5-97f6-8e44afb09ffa'
    layer_id = 'f229593c-feb4-43a8-8259-d7618244a3bc'

    color_map_list = [
        'N-GREENG', 'N-R2', 'N-R3', 'T', 'N-AVHRR', 'JG', 'BW',
        'RW-LEGACY', 'GRANULAR', 'GM-COMP1', 'GM-RGB3', 'GM-QUAD',
        'CVC', 'CHS_HC2', 'CHS_HC1', 'SMWE', '10 Class Agroprecision Grey',
        '6 Class Agroprecision', '6 Class Agroprecision Grey',
        '10 Class Agroprecision', 'CHS-LEGACY', 'TRICOLOR', 'TWE'
    ]

    for color_map in color_map_list:
        out_file_name = os.path.join(output_dir, color_map + '.tiff')

        request_url = (
            'https://api.terravion.com/v1/layers/' + layer_id +
            '/geotiffs/image.tiff?colorMap=' + color_map +
            '&access_token=' + access_token
        ).replace(' ', '%20')

        print(request_url)

        request = Request(request_url)
        response_file = urlopen(request)

        try:
            print('writing ' + str(out_file_name))
            with open(out_file_name, 'wb') as local_file:
                local_file.write(response_file.read())

        except HTTPError as e:
            print("HTTP Error:", e.code)

        except URLError as e:
            print("URL Error:", e.reason)


if __name__ == '__main__':
    main(sys.argv[1:])
