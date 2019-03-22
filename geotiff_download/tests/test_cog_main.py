import os
import json
import logging
import tests.root_env
from lib.cog_raster_lib import CogRasterLib
logging.basicConfig(level=logging.INFO)
class TestCogMain(object):
    def test_validate_terravion_cog(self):
        input_tif = 's3://cog-terravion-com/f4e8dfd0-ab45-4299-b2cb-98142c0f1b2b_PB_COG.tif'
        cr_lib = CogRasterLib()
        if cr_lib.validate_terravion_cog(input_tif):
            assert True
        else:
            assert False

