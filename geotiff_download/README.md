geotiff_download
====================

Request api@terravion.com for an access_token

## Example Command Lines:

**Retrieve all the blocks:**

`python main.py -user_name <email> -access_token <access_token> -get_block_list True`

**Retrieve download links by block id:**

`python main.py -user_name <email> -access_token <access_token> -block_id_list <bid1> <bid2> <...> -download_multiband True`

**Retrieve download links by block_name:**

`python main.py -user_name <email> -access_token <access_token> -block_name <block_name> -download_multiband True`

**Retrieve avaliable layers by block_name:** 

`python main.py -user_name <email> -access_token <access_token> -block_name <block_name>`

**Retrieve avaliable layers by lat lng:**

`python main.py -user_name <email> -access_token <access_token> -lat <lat> -lng <lng>`