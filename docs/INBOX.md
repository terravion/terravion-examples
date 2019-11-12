## Working with Inbox

> Inbox currently retrieves delivered layers sorted by date.

### ENDPOINT

`POST /layers/getLayersByDate`

### OPTIONS

| Parameter| Required | Description | Type |
| - | - | - | - |
| userId | true | TerrAvion User ID | String |
| inboxSettings | true | formData | Object |


***inboxSettings***
```
{
  "filter": {
    "unread": false,
    "starred": false,
    "agronomist": [],
    "farmer": [],
    "farm": [],
    "order": [],
    "plan": []
  },
  "page":1
}
```

### EXAMPLE

```
curl -X POST --header "Accept: application/json" -d "{
  \"showFilter\": false,
  \"page\": 1,
  \"maxPage\": null,
  \"loading\": false
}" "https://api2.terravion.com/layers/getLayersByDate?\
userId=YOUR_USER_ID\
&access_token=YOUR_ACCESS_TOKEN"
```

### RESULT

```
{
  "layers": [
    {
      "layerId": "0c8b8fcb-2fd5-4ea7-9812-aa4f2bceb43b",
      "layerName": "b0795ca0-95db-4fe1-a744-6a547bf8c41f",
      "layerDateEpoch": 1569259980.154,
      "layerStatus": "DELIVER",
      "blockId": "fce86d84-aae4-4376-8c08-bd8883e96810",
      "blockName": "SW__Irrigated/S6 NW 29-32-31",
      "userLayerId": "0f04fd89-4c43-407a-8be1-abd2b7ec1b7b",
      "userLayerStatus": "UNREAD",
      "userLayerMeta": null,
      "season": [
        "2018",
        "2019"
      ]
    }
  ]
}
```