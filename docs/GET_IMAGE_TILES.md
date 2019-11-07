## Get image tiles

> Tiles to source to your mapping app.

### ENDPOINT

`GET /users/{id}/{z}/{x}/{y}.png`

### OPTIONS

| Parameter| Required | Description | Type |
| - | - | - | - |
| user |  true  | TerrAvion User ID | String |
| z | true  | Tile Zoom Level | Integer |
| x | true | Tile x-axis position | Integer |
| y | true | Tile Y-axis position | Integer |
| tms | false | Default: true | Boolean |
| t | false | Histogram threshold | String |
| a | false | Low threshold parameter | Double |
| b | false | High threshold parameter | Double |
| product | false | Product Type (NC, CIR, NDVI, TIRS, etc.) | String |
| colorMap | false | Color Map to apply for NDVI, ZONE, TIRS Example: N-R2, ,N-R3,N-AVHRR, T, N  Default: NONE. | String |
| epochStart | false | Start date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer |
| epochEnd | false | End date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer |
| dataJSON | false | | String |
| useSentinel2Scale | false | flag to indicate using sentinel 2 scale | Boolean |
| equation | false | Veg Index Equation (eg. ((B4-B6)/(B4+B6))) | String |
| lowerBound | false | Lower contrast boundary (16bit) | Double |
| upperBound | false | Upper contrast boundary (16bit) | Double |
| lowDegC | false | Lower thermal temperature boundary | Double |
| highDegC | false | Upper thermal temperature boundary | Double |
| blockId | false | TerrAvion Block ID | String |
| useAutoBounds | false |  | Boolean |

## EXAMPLE

```
curl -X POST "https://api2.terravion.com/users/YOUR_USER_ID\
/16/14498/40135.png.png?\
tms=true&product=NC&\
epochStart=1568828725&epochEnd=1569001525&\
lowerBound=1660&upperBound=4364&\
access_token=YOUR_ACCESS_TOKEN" >> example.png
```

## RESULT

```
A PNG TILE
```

## MORE EXAMPLES

1. [Google Maps](../examples/image_tiles/terravion_gmap_example.html)
2. [Mapbox](../examples/image_tiles/terravion_mapbox_example.html)
3. [MapboxGL](../examples/image_tiles/terravion_mapbox_gl_example.html)
4. [Leaflet](../examples/image_tiles/terravion_leaflet_example.html)
5. [Leaflet Dynamic](../examples/image_tiles/terravion_leaflet_example_with_dynamic_colormap.html)
6. [Leaflet Cog](../examples/image_tiles/terravion_cog_leaflet_example.html)
7. [Cesium](../examples/image_tiles/terravion_cesium_example.html)
8. [Open Layers](../examples/image_tiles/terravion_openLayers_example.html)