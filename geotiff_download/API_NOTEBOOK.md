# API NOTEBOOK

## What you need:

### 1. An access token and userId

1. you can start using our sales_demo@terravion.com token

```
03uKC6WwDrVUfh4jFrANmEMUegXApJXTeEYrGQc9Rf1ViWtByZEIMQ43CIepS7Cg
```
        
2. you can ask for your own token to support@terravion.com

### 2. Your userId

1. If you are using our sales_demo@terravion.com your `userId` would be

```
1455cf90-af48-4fae-87d0-57523de51b8b
```
    
2. Using your own token you can get the userId with the following call

```
curl -X GET --header "Accept: application/json" "https://api2.terravion.com/users/getUserId?access_token=YOUR_ACCESS_TOKEN"
```

* which retrieve the following result

```
{
  "userId": "7fd1da8b-a067-48e5-ab04-84ab6645409b"
}
```

## Single Geotiff Download

> This call allows you to request one geotiff for a selected layer  .
> As a result it will generate a task_id which will allow you to access your download once ready.

### ENDPOINT

`POST /tasks/requestGeotiffTask`

### OPTIONS

| Parameter | Required | Description | Data Type |
| - | - | - | - |
| userId | true | | string |
| userId | true | | string |
| colorMap | false |  | string |
| isColormapRgb | false |  | string |
| epsgCode | false |  | double |
| multiband | false |  | boolean |

### EXAMPLE
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

## Get tiles for map

### ENDPOINT

`GET /users/{id}/{z}/{x}/{y}.png`

### OPTIONS

| Parameter| Required | Description | Type | 
| - | - | - | - |
| user |  true  | user id | String | 
| z | true  | Tile Zoom Level | Integer | 
| x | true | Tile x-axis position | Integer | 
| y | true | Tile Y-axis position | Integer | 
| tms | false | Default true | Boolean |
| t | false | threshold | String |
| a | false | low threshold parameter | Double |
| b | false | high threshold parameter | Double |
| product | false | Product Type (NC, CIR, NDVI, TIRS, ZONE) | String | 
| colorMap | false | Color Map to apply for NDVI, ZONE, TIRS Example: N-R2, ,N-R3,N-AVHRR, T, N  Default: NONE. | String |  
| epochStart | false | Start date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer | 
| epochEnd | false | End date in Epoch time (seconds since 1970-01-01T00:00:00Z) | Integer | 
| dataJSON | false | | String |
| useSentinel2Scale | false | flag to indicate using sentinel 2 scale | Boolean |
| equation | false | | String |
| lowerBound | false | | Double |
| upperBound | false | | Double |
| lowDegC | false | | Double |
| highDegC | false | | Double |
| blockId | false | | String |
| useAutoBounds | false | | Boolean |


| access_token | | acess_token (contact api@terravion.com for access) | Text | 

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