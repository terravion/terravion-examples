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

> Tiles to source to your mapping app.

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

## Checking the delivery status

> Use TerrAvion Delivery Tracking API to track the delivery status of your field. 

### ENDPOINT

`GET /users/{id}/getDeliveryTracking`

### OPTIONS

| Parameter| Required | Description | Type | 
| - | - | - | - |
| blockId | false | | String |
| userId | false | | String |
| fieldName | false | | String |
| serviceCycleStartEpoch | false | | Double |
| serviceCycleEndEpoch | false | | Double |
| serviceDateEpoch | false | | Double |
| year | false | | String |
| farmerId | false | | String |
| agronomistId | false | | String |
| useCurrentCycle | false | | Boolean |
| offset | false | | Double |
| limit | false | | Double |
| getCount		 | false | | Boolean|
| adminMode | false | | String |
| serviceId | false | | String |
| planId | false | | String |
| boOrderId | false | | String |
| partnerOrderId | false | | String |

### EXAMPLE

```
curl -X GET --header "Accept: application/json" "http://api2.terravion.com/users/\
YOUR_USER_ID/getDeliveryTracking?\
access_token=YOUR_ACCESS_TOKEN"
```

### RESULT

```
[
  {
    "serviceId": "fb25ade9-a93f-461f-be41-0a34eadbf3af",
    "serviceStart": "2019-03-17",
    "serviceEnd": "2019-04-20",
    "serviceName": "2019 Winter Wheat",
    "season": "2019",
    "farmerEmail": "John.Doe@email.com",
    "farmerLastName": "John",
    "farmerFirstName": "Doe",
    "agronomistEmail": "Joe.Public@gmail.com",
    "agronomistFirstName": "Joe",
    "agronomistLastName": "Public",
    "fieldName": "NW 12-33-32",
    "planId": "6492eb94-867e-457b-a570-7c9115519f0c",
    "orderDate": "2019-03-22T19:21:33.315Z",
    "blockId": "4f31309c-5346-4c89-89a8-8d9a4387c516",
    "meta": {
      "src": "EFC",
      "farm_name": "NW Farms",
      "grower_id": "a01d04bb-a6ea-4165-b2b0-fee0f61a5c9d",
      "location_id": "4afafab3-a25f-442f-b269-70d177c47137",
      "farm_id": "8bd278b6-cf1d-43e2-9b23-1b42945056e2",
      "field_id": "db68a65c-291f-4ee3-a886-8e4e56879774",
      "field_name": "NW12-33-32",
      "last_edited_at": "2019-03-22T21:22:42.965Z"
    },
    "acres": 123.915450593026,
    "partnerOrderId": null,
    "serviceCycleBlockOrderId": "188dc421-e363-4194-b62e-d6b9fa605630",
    "priority": 0,
    "deliveryStatus": "DELIVER",
    "flightStatus": "DELIVER",
    "addDate": "2019-03-22T19:22:12.253Z",
    "modifyDate": "2019-04-19T02:02:33.332Z",
    "serviceCycleId": "11a93c1c-884a-4d10-a32f-ed0ebc10703c",
    "captureDate": "2019-04-12T17:40:54.295Z",
    "captureEpoch": 1555090854.295,
    "deliveryAddDate": "2019-04-13T10:01:09.541Z",
    "deliveryAddEpoch": 1555149669.54158,
    "fieldServiceAddDate": "2019-03-22T19:21:33.343Z",
    "orderedBeforeCycle": false,
    "orderedDuringCycle": true
  }
]
```

## Working with Notes/ Pins

> You can add/ edit/ delete Notes in different ways interactively on our maps through our API.  
> Every note will therefore, be binded to a specific set of coordinates.  
> Note: for the time being you can add Images only through our app.

### ENDPOINTS

`POST /features/storePin` => Store a single Pin

`GET /features/getAllPins` => Get all your existing Pins

`GET /features/getPins` => Get all pins related to a single LayerID

`GET /features/getPinData` => Get data related to a single Pin

`GET /features/{featureId}/thumb.jpg` => Get image related to a single Pin

`GET /features/deletePin` => Delete a single Pin

### EXAMPLE

```
curl -X GET --header "Accept: application/json" "http://api2.terravion.com/features/getAllPins?\
userId=YOUR_USER_ID\
&access_token=YOUR_ACCESS_TOKEN"
```

### RESULT

```
[
  {
    "block_id": "6884bb81-c9a1-4473-9174-fb5d057dfa27",
    "feature_id": "28a3083d-c0c7-ebd7-c215-1d6bbd02b34e",
    "meta": {
      "title": "Common rust 3rd leaf below tassels",
      "url": "https://user-upload-terravion-com.s3.amazonaws.com/overview-app/28a3083d-c0c7-ebd7-c215-1d6bbd02b34e.jpeg"
    },
    "add_date": "2019-07-06T23:56:55.277Z",
    "creator_user_id": "003be027-bdc1-4a05-96a8-b8b8976abaea",
    "st_asgeojson": "{\"type\":\"Point\",\"coordinates\":[-99.710712488215,37.2586363652761]}",
    "first_name": "Joe",
    "last_name": "Public"
  }
]
```