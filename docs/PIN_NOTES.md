## Intro

The Pin Notes feature help our user to mark a point on any of their fields and add notes and images to it. Then every person who has access to that field can view that note. Also they can share that note's content to people outside our infrastructure.

In order to create a note you will need a coordinate pair -latitude and longitude- and at least a title, text or image.

## Assumptions

1. You already went through our [Get Started](GET_STARTED.md) doc.
2. That you know what's the block_id that you want to insert a note for (same doc).

### ENDPOINTS & OPTIONS

#### `POST /features/storePin` => Store a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| data | false | formData | String |

***Sample formData***
```
{
  meta: {
    title, text
  },
  imageMeta: {
    url
  },
  st_asgeojson: {
    type: "Point",
    coordinates: [longitude, latitude]
  },
  block_id,
  feature_id: uuid,
  userId,
  add_date: 2018-10-14T15:19:31.073Z
}
```
***`uuid` python example***

```
>>> import uuid

>>> # make a random UUID
>>> uuid.uuid4()

UUID('16fd2706-8baf-433b-82eb-8c7fada847da')
```

---

#### `POST /features/storePinImage` => Store image for Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| data | false | formData | String |

***Sample formData***
```
{
  uri: base64_encoded_image
  name,
}
```

---

#### `GET /features/getAllPins` => Get all your existing Pins

| Parameter| Required | Description | Type |
| - | - | - | - |
| userId | false | | String |

***Sample Response***
```
[
  {
    "block_id": "99cd2c6e-e61f-c88f-981d-decc7e8e79c2",
    "feature_id": "0404cd00-bf51-4c3e-7186-f7780924a8cb",
    "meta": {
      "title": "IDC",
      "text": ""
    },
    "add_date": "2019-09-12T00:21:13.285Z",
    "creator_user_id": "0d4eae7e-43ce-4574-8ec4-270881bab6d1",
    "st_asgeojson": "{\"type\":\"Point\",\"coordinates\":[-101.60236709429,35.6356264849986]}",
    "first_name": "Joe",
    "last_name": "Doe"
  },
  ...
]
```
---

#### `GET /features/getPins` => Get all pins related to a single LayerID

| Parameter| Required | Description | Type |
| - | - | - | - |
| blockId | false | formData | String |

---

#### `GET /features/getPinData` => Get data related to a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | formData | String |

---

#### `GET /features/{featureId}/thumb.jpg` => Get image related to a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | formData | String |

---

#### `GET /features/deletePin` => Delete a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | formData | String |

### EXAMPLE

```
curl -X GET --header "Accept: application/json" "https://api2.terravion.com/features/getAllPins?\
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