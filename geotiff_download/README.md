geotiff_download
====================

Request api@terravion.com for an access_token

## Example Command Lines:

**Retrieve all the blocks:**

`python main.py -user_name <email> -access_token <access_token> -get_block_list True`

**Retrieve download links by block id:**

`python main.py -user_name <email> -access_token <access_token> -block_id_list <bid1> <bid2> <...> -product MULTIBAND`

**Retrieve download links by block_name:**

`python main.py -user_name <email> -access_token <access_token> -block_name <block_name> -product MULTIBAND`
