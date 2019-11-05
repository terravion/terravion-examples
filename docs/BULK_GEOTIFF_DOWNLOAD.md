## Bulk Geotiff Download

> This call allows you to request all the geotiffs for your layers on a given time range.  
> As a result it will generate a task_id which will allow you to access your download once ready.

### ENDPOINT

`POST /tasks/requestGeotiffTaskBulkRequest`

### OPTIONS

| Parameter | Required | Description | Data Type |
| - | - | - | - |
| userId | true | | string |
| dateFilterStart | true | YYYY-MM-DD | string |
| dateFilterEnd | true |YYYY-MM-DD | string |
| colorMap | false |  | string |
| isColormapRgb | false |  | string |
| epsgCode | false |  | double |
| multiband | false |  | boolean |

### EXAMPLE
```
curl -X POST --header "Content-Type: application/json" "https://api2.terravion.com/\
tasks/requestGeotiffTaskBulk?\
userId=YOUR_USER_ID&\
dateFilterStart=YYYY-MM-DD&\
dateFilterEnd=YYYY-MM-DD&\
multiband=true&\
access_token=YOUR_ACCESS_TOKEN"
```
### RESULT
```
{
  "task_id": "2b5589b5-acbc-42a6-9fa1-9b6c6d1adee4"
}
```