geotiff_download [main.py]
====================

Request api@terravion.com for an access_token

## Example Command Lines:

**Retrieve all the blocks:**

`python main.py -user_name <email> -access_token <access_token> -get_block_list True`

**Retrieve download links by block id:**

`python main.py -user_name <email> -access_token <access_token> -block_id_list <bid1> <bid2> <...> -product MULTIBAND`

**Retrieve download links by block_name:**

`python main.py -user_name <email> -access_token <access_token> -block_name <block_name> -product MULTIBAND`


cloud optimized geotiff download [cog_main.py]
====================

In order to leverage cloud optimized geotiff and use this example code, gdal and rasterio must be downloaded. 

https://www.gdal.org/


Installing gdal on mac:
http://www.kyngchaos.com/software/frameworks/




Run tests to check out example usage