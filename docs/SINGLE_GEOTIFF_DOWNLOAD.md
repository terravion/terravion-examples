# Single Geotiff Download

## 1. Get Layers From BlockId

> This call allows you to get all layers corresponding to a single BlockId.

### ENDPOINT

`GET /layers/getLayersFromBlockId`

### OPTIONS

| Parameter | Required | Description | Data Type |
| - | - | - | - |
| blockId | true | Block ID | string |
| userId	| false | Terravion User ID | string |
| useSentinel2Scale | false |  | boolean |
| year | false |  | double |	
| epochStart | false |  | double |	
| epochEnd | false |  | double |	

### REQUEST EXAMPLE
```
curl -X POST --header "Content-Type: application/json" "https://api2.terravion.com/\
layers/getLayersFromBlockId?\
blockId=6e114e54-d726-428f-a562-b99c81c49909&\
access_token=YOUR_ACCESS_TOKEN"
```
### RESULT
```
[
  {
    "blockId": "6e114e54-d726-428f-a562-b99c81c49909",
    "ncLayerId": "08b5d633-f4e0-4409-a120-1577cfb47e31",
    "ncLayerName": "ac69211a-74e6-4822-aab6-fad62ba57887",
    "ndviLayerId": "e3ae9178-8775-4150-9564-5718c1f1938f",
    "ndviLayerName": "ac69211a-74e6-4822-aab6-fad62ba57887",
    "cirLayerId": "f9fc5a46-9272-4c9b-b801-0165d0c587e1",
    "cirLayerName": "ac69211a-74e6-4822-aab6-fad62ba57887",
    "zoneLayerId": "6d64c516-6437-4894-a99d-66f60b5d22bb",
    "zoneLayerName": "ac69211a-74e6-4822-aab6-fad62ba57887",
    "thermalLayerId": "ad7b5b30-fc09-463b-a36f-c764f5f44b4e",
    "thermalLayerName": "ac69211a-74e6-4822-aab6-fad62ba57887",
    "syntheticNCLayerId": "7334b2ad-41ed-45b9-8b85-8552f10623ff",
    "panTIRSLayerId": null,
    "layerDateEpoch": 1562790257.672,
    "addDateEpoch": 1562857968.20289,
    "sunAngle": "74.31001310438626",
    "ndviMean": 0.1279,
    "ndviStd": 0.1264,
    ...
  }
]
```

## 2. Request Geotiff Task

> This call allows you to request a geotiff for a selected layer. As a result it will generate a task_id which will allow you to access your download once ready.

### ENDPOINT

`POST /tasks/requestGeotiffTask`

### OPTIONS

| Parameter | Required | Description | Data Type |
| - | - | - | - |
| userId | true | TerrAvion User ID | string |
| layerId | true | TerrAvion Layer ID | string |
| colorMap | false | Specified colormap | string |
| isColormapRgb | false | RGB Flag | string |
| epsgCode | false | EPSG Code (eg. 4326) | double |
| multiband | false | Download an unprocessed multiband GeoTIFF | boolean |

### REQUEST EXAMPLE
```
curl -X POST --header "Content-Type: application/json" "https://api2.terravion.com/\
tasks/requestGeotiffTask?\
userId=YOUR_USER_ID&\
layerId=SELECTED_LAYER_ID&
multiband=true&\
access_token=YOUR_ACCESS_TOKEN"
```
### RESULT
```
{
  "task_id": "2b5589b5-acbc-42a6-9fa1-9b6c6d1adee4"
}
```

## 3. Check Geotiff Task Status

> This call allows you to check the status of your geotiff task, and when it's ready to download it exposes the download endpoint.

### ENDPOINT

`GET /tasks/getUserDownloads`

### OPTIONS

| Parameter | Required | Description | Data Type |
| - | - | - | - |
| userId | true | TerrAvion User ID | string |

### REQUEST EXAMPLE
```
curl -X POST --header "Content-Type: application/json" "https://api2.terravion.com/\
tasks/getUserDownloads?\
userId=YOUR_USER_ID&\
access_token=YOUR_ACCESS_TOKEN"
```

## 4. Download Geotiff

> This call allows you to download the requested geotiff once it's ready.

### ENDPOINT

`GET /tasks/downloadSingleGeotiff/YOUR_TASK_ID.tiff`

### OPTIONS

| Parameter | Required | Description | Data Type |
| - | - | - | - |
| taskId | true | Single Geotiff Download Task ID | string |

### REQUEST EXAMPLE
```
wget -O YOUR_FILE_NAME.tiff "https://api2.terravion.com/\
tasks/downloadSingleGeotiff/YOUR_TASK_ID.tiff&\
access_token=YOUR_ACCESS_TOKEN"
```

### MORE EXAMPLES

* [Geotiff Download Python Script](../examples/geotiff_download)
