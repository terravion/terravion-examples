# terravion-examples

This repository contains example codes to use [TerrAvion's API](http://docs.terravionv1.apiary.io/#)
Pleaese contact support@terravion.com for your access_token.

[TerrAvion API Tile Request Endpoint] (http://docs.terravionv1.apiary.io/#reference/layers/usersuseridoremaillayerstileszxypngcolormapepochstartepochendproduct/get)
====================
End Point Specification 
-------------------
https:/api.terravion.com/v1/users/**\<userIdOrEmail\>**/layers/tiles/**\<z\>**/**\<x\>**/**\<y\>**.png?colorMap=**\<colorMap\>**&epochStart=**\<epochStart\>**&epochEnd=**\<epochEnd\>**&product=**\<product\>**access_token=**\<access_token\>**

The following is are the parameters of the end point 

Parameter| Description | Type 
--- | --- | ---
userIdOrEmail | id or email of the user | Text 
product| Product Type | Text
epochStart| Start date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer
epochEnd| End date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer
z| Tile Zoom Level | Integer
x| Tile x-axis position | Integer
y| Tile Y-axis position | Integer 
colorMap| Color Map to apply for NDVI, ZONE, TIRS Example: N-R3.Default: NONE. | Text 
access_token| acess_token (contact support@terravion.com for access) |Text

Integrating TerrAvion Tiles with Google Maps 
--------------------
If you host your own map application with Google Maps as a base layer, you may directly pull png tiles from TerrAvion's API. Note that TerrAvion API TMS tile coordinate system needs to be translated to match Google Map tiles system in the y-axis. `Math.pow(2,zoom)-coord.y-1` More info: http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

The following is an example html that pulls tiles from support+demo@terravion.com's account which has the [sample academic blocks] (https://maps.terravion.com/#/demo). 

[terravion_gmap_example.html](https://github.com/terravion/terravion-examples/blob/master/terravion_gmap_example.html)

Integrating Terravion Tiles with Leaflet 
--------------------
If you host your own Leaflet map application, you may directly pull the png tiles from TerrAvion's API, the following is an simple example with toggle to different product. Note that in leaflet, the TMS options needs to be true for TerrAvion tiles to show up correctly. `tms: true`

[terravion_leaflet_example.html](https://github.com/terravion/terravion-examples/blob/master/terravion_leaflet_example.html)

Geotiff Download 
====================
Downloading geotiff from TerrAvion API is easy, simply run the following python script to streamline the process.

-get the blocks 

-get the layers 

-download the imagery 

[terravion_api_bulk_download.py](https://github.com/terravion/terravion-examples/blob/master/terravion_api_bulk_download.py)
