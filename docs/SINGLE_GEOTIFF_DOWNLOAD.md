## Single Geotiff Download

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
tasks/requestGeotiffTaskBulk?\
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

### CHECK DOWNLOAD EXAMPLE
```

```
### RESULT
```

```

### MORE EXAMPLES

* [Geotiff Download Python Script](../examples/geotiff_download)
