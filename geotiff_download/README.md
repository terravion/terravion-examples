geotiff_download [main.py]
====================

Request api@terravion.com for an access_token

## Example Command Lines:

**Retrieve all the blocks:**

`python main.py -access_token <access_token> -get_block_list True`

**Retrieve download links by block id:**

`python main.py -access_token <access_token> -block_id_list <bid1> <bid2> <...> -product MULTIBAND`

Add --working_dir <working_dir> to download actual image

**Retrieve download links by block_name:**

`python main.py -access_token <access_token> -block_name <block_name> -product MULTIBAND`

Add --working_dir <working_dir> to download actual image

cloud optimized geotiff download [cog_main.py]
====================

In order to leverage cloud optimized geotiff and use this example code, gdal and rasterio must be downloaded. 

https://www.gdal.org/


Installing gdal on mac:
http://www.kyngchaos.com/software/frameworks/

Intalling rasterio:
https://rasterio.readthedocs.io/en/stable/installation.html

**Print account summary**

`python cog_main.py --access_token <access_token> --get_summary`

**Preview download multiband**

`python cog_main.py --access_token <access_token> --get_layers`

**Download multiband to working_dir**

`python cog_main.py --access_token <access_token> --get_layers --working_dir <working_dir>`

Run tests to check out example usage