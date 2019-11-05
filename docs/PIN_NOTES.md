## Working with Notes/ Pins

> You can add/ edit/ delete Notes in different ways interactively on our maps through our API.  
> Every note will therefore, be binded to a specific set of coordinates.  
> Note: for the time being you can add Images only through our app.

### ENDPOINTS & OPTIONS

`POST /features/storePin` => Store a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| data | false | formData | String |

`GET /features/getAllPins` => Get all your existing Pins

| Parameter| Required | Description | Type |
| - | - | - | - |
| userId | false | formData | String |

`GET /features/getPins` => Get all pins related to a single LayerID

| Parameter| Required | Description | Type |
| - | - | - | - |
| blockId | false | formData | String |

`GET /features/getPinData` => Get data related to a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | formData | String |

`GET /features/{featureId}/thumb.jpg` => Get image related to a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | formData | String |

`GET /features/deletePin` => Delete a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | formData | String |

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