TerrAvion Examples
====================
This repository contains example codes to use [TerrAvion's API](https://api2.terravion.com/)

Pleaese contact [api@terravion.com](api@terravion.com) for your access_token.

There are two types of integration avaliable for accessing TerrAvion Imagery.
- Geotiff Download
- Tiles Integration

Cloud Optimized Geotiff Download
====================
TerrAvion's cloud optimized geotiff is avaliable for partners for download through TerrAvion's API. 

See [Documentation](https://github.com/terravion/terravion-examples/tree/master/geotiff_download#cloud-optimized-geotiff-download-cog_mainpy) for more information.


TerrAvion v2 Tiles End Point Specification
====================
[TerrAvion API Tile Request Endpoint Documentation](https://api2.terravion.com/#operation/TaUser.prototype.layerTiles)

https://api2.terravion.com/users/<userId\>/<z\>/<x\>/<y\>.png?colorMap=<colorMap\>&epochStart=<epochStart\>&epochEnd=<epochEnd\>&product=<product\>&access_token=<access_token\>

The following is are the parameters of the end point 

Parameter| Description | Type 
--- | --- | ---
user | user id | Text 
product| Product Type (NC, CIR, NDVI, TIRS, ZONE) | Text
epochStart| Start date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer
epochEnd| End date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer
z| Tile Zoom Level | Integer
x| Tile x-axis position | Integer
y| Tile Y-axis position | Integer 
colorMap| Color Map to apply for NDVI, ZONE, TIRS Example: N-R2, ,N-R3,N-AVHRR, T, N  Default: NONE. | Text 
access_token| acess_token (contact api@terravion.com for access) |Text

Integrating TerrAvion Tiles with Google Maps 
====================
If you host your own map application with Google Maps as a base layer, you may directly pull png tiles from TerrAvion's API. Note that TerrAvion API TMS tile coordinate system needs to be translated to match Google Map tiles system in the y-axis. `Math.pow(2,zoom)-coord.y-1` More info: http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

The following is an example html that pulls tiles from support+demo@terravion.com's (5bad4dfa-7262-4a0a-b1e5-da30793cec65) account which has the [sample academic blocks] (https://maps.terravion.com/#/demo). From the "Hello World" code of [Google Maps Javascript API Getting Started] (https://developers.google.com/maps/documentation/javascript/tutorial#The_Hello_World_of_Google_Maps_v3), you simply need to add the following code snippet to include TerrAvion's png tiles: 

```javascript
  var user_id = '5bad4dfa-7262-4a0a-b1e5-da30793cec65'; // support+demo@terravion.com
  var access_token = '2e68cee0-b2fd-4ef5-97f6-8e44afb09ffa'
  var epochStart = '1456200627'
  var epochEnd = '1456632627'
  var terravion_nc = new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {
      var tileUrl = 'https://api2.terravion.com/users/'
      tileUrl += user_id+'/'+zoom+'/'+coord.x+'/'+(Math.pow(2,zoom)-coord.y-1)+'.png'
      tileUrl += '?product=NC'
      tileUrl += '&epochStart=' + epochStart
      tileUrl += '&epochEnd=' + epochEnd
      tileUrl += '&access_token=' + access_token
      return tileUrl
    },
    tileSize: new google.maps.Size(256, 256),
    isPng: true ,
    maxZoom: 19,
    minZoom: 0,
    name: 'nc'
  });
  map.overlayMapTypes.push(terravion_nc);
```

code: 
<a href="https://github.com/terravion/terravion-examples/blob/master/examples/image_tiles/terravion_gmap_example.html" target="_blank">terravion_gmap_example.html</a>


preview: 
<a href="https://rawgit.com/terravion/terravion-examples/master/examples/image_tiles/terravion_gmap_example.html" target="_blank">terravion_gmap_example.html</a>

Integrating Terravion Tiles with Leaflet 
--------------------
If you host your own Leaflet map application, you may directly pull the png tiles from TerrAvion's API, the following is an simple example with toggle to different product. Note that in leaflet, the TMS options needs to be true for TerrAvion tiles to show up correctly. `tms: true`

```javascript
  var access_token='2e68cee0-b2fd-4ef5-97f6-8e44afb09ffa'
  var user_id='5bad4dfa-7262-4a0a-b1e5-da30793cec65' // support+demo@terravion.com
  var epochStart='1456200627'
  var epochEnd='1456632627'
  var tileUrlTemplate = apiUrl + '/users/'+ user_id
  tileUrlTemplate += '/{z}/{x}/{y}.png'
  tileUrlTemplate += '?epochStart='+epochStart+'&epochEnd='+ epochEnd
  tileUrlTemplate += '&access_token='+access_token;

  L.tileLayer(tileUrlTemplate + '&product=NC', {
    attribution: 'TerrAvion',
    maxZoom: 19,
    tms: true
  }).addTo(mymap);
```

code: 
<a href="https://github.com/terravion/terravion-examples/blob/master/examples/image_tiles/terravion_leaflet_example.html" target="_blank">terravion_leaflet_example.html</a>

preview: 
<a href="https://rawgit.com/terravion/terravion-examples/master/examples/image_tiles/terravion_leaflet_example.html" target="_blank">terravion_leaflet_example.html</a>

OpenLayers Example
====================
code: 
<a href="https://github.com/terravion/terravion-examples/blob/master/examples/image_tiles/terravion_openLayers_example.html" target="_blank">terravion_openLayers_example.html</a>

preview: 
<a href="https://rawgit.com/terravion/terravion-examples/master/examples/image_tiles/terravion_openLayers_example.html" target="_blank">terravion_openLayers_example.html</a>

<a href="https://terravion.github.io/terravion-examples/cog_tiles_integration/terravion_cog_leaflet_example.html" target="_blank">Example Sandbox</a>


TerrAvion API2 Dynamic Colormap tiles endpoint
====================
Parameter| Description | Type | Required
--- | --- | --- | --
userIdOrEmail | id or email of the user | Text | True
product| Product Type (NC,CIR,NDVI,TIRS, ZONE) | Text | True
epochStart| Start date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer | True
epochEnd| End date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer | True
z| Tile Zoom Level | Integer | True
x| Tile x-axis position | Integer | True
y| Tile Y-axis position | Integer | True
colorMap| Color Map to apply for NDVI, ZONE, TIRS Example: N-R2, ,N-R3,N-AVHRR, T, N  Default: NONE. | Text | False
access_token| acess_token (contact api@terravion.com for access) | Text | True
a | Min Colormap Threshold (0~255) | Number | False
b | Max Colormap Threshold (0~255) | Number | False

code: 
<a href="https://github.com/terravion/terravion-examples/blob/master/examples/image_tiles/terravion_leaflet_example_with_dynamic_colormap.html" target="_blank">terravion_leaflet_example_with_dynamic_colormap.html</a>

preview: 
<a href="https://rawgit.com/terravion/terravion-examples/master/examples/image_tiles/terravion_leaflet_example_with_dynamic_colormap.html" target="_blank">terravion_leaflet_example_with_dynamic_colormap.html</a>

Automatic Colormap Flow
====================
1. Specify the userId, blockId, product, epochstart, epochEnd of the histogram to use for colormap.
2. Call https://api2.terravion/layerStats/getColormapThresholds/ endpoint with accessToken to get the colormap adjustment parameter, a (low) and b (high).
3. Add the a and b parameter into the tiles call using api2 tiles api endpoint to get dynamic colormap. 

See the example above. If you have any questions, email api@terravion.com for support. 


Legacy Tasked-Based Geotiff Download 
====================
API partners may use tasked based geotiff download to access TerrAvion's imagery. 

[main.py](https://github.com/terravion/terravion-examples/blob/master/geotiff_download/main.py)

Workflow overview:
1. get the blocks/fields 
2. get the layers 
3. download the imagery 
