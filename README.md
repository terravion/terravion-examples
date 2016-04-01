# terravion-examples

This repository contains example codes to use [TerrAvion's API](http://docs.terravionv1.apiary.io/#)
Pleaese contact wmaio@terravion.com for your access_token.

Downloading Geotiff 
====================
Downloading many geotiff from [TerrAvion Overview Web App] (https://maps.terravion.com/) can be challenging, the following python script helps you streamline the process.

[terravion_api_bulk_download.py](https://github.com/terravion/terravion-examples/blob/master/terravion_api_bulk_download.py)

Integrating TerrAvion Tiles with Google Maps 
====================
If you host your own map application with Google Maps as a base layer, you may directly pull the png tiles from TerrAvion's API, the following is an simple example. Note that TerrAvion API TMS tile coordinate system needs to be translated to match Google Map tiles system in the y-axis. `Math.pow(2,zoom)-coord.y-1` More info: http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

[terravion_gmap_example.html](https://github.com/terravion/terravion-examples/blob/master/terravion_gmap_example.html)

Integrating Terravion Tiles with Leaflet 
====================
If you host your own Leaflet map application, you may directly pull the png tiles from TerrAvion's API, the following is an simple example with toggle to different product. Note that in leaflet, the TMS options needs to be true for TerrAvion tiles to show up correctly. `tms: true`

[terravion_leaflet_example.html](https://github.com/terravion/terravion-examples/blob/master/terravion_leaflet_example.html)
