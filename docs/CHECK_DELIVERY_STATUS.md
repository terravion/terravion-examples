## Check delivery status

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
