## Intro

The Pin Notes feature help our user to mark a point on any of their fields and add notes and images to it. Then every person who has access to that field can view that note. Also they can share that note's content to people outside our infrastructure.

In order to create a note you will need a coordinate pair -latitude and longitude- and at least a title, text or image.

## Assumptions

1. You already went through our [Get Started](GET_STARTED.md) doc.
2. That you know what's the block_id that you want to insert a note for (same doc).

## Note

The pin note identifier is called Feature ID.

### ENDPOINTS & OPTIONS

#### `GET /features/getAllPins` => Get all your existing Pins

| Parameter| Required | Description | Type |
| - | - | - | - |
| userId | false | | String |

***Python example***
```
import urllib2

def get_all_pins():
    base_url = 'https://api2.terravion.com/'
    method = 'features/getAllPins'
    user_id = 'YOUR_USER_UD'
    access_token = 'YOUR_ACCESS_TOKEN'
    url = base_url + method
    url += '?userId=' + user_id
    url += '&access_token=' + access_token
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

get_all_pins()
```
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

#### `GET /features/getPins` => Get all pins related to a single Block ID

| Parameter| Required | Description | Type |
| - | - | - | - |
| blockId | false |  | String |

***Python example***
```
import urllib2

def get_pins_by_block_id():
    base_url = 'https://api2.terravion.com/'
    method = 'features/getPins'
    block_id = 'YOUR_BLOCK_ID'
    access_token = 'YOUR_ACCESS_TOKEN'
    url = base_url + method
    url += '?blockId=' + block_id
    url += '&access_token=' + access_token
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

get_pins_by_block_id()
```

***Sample Response***
```
[
  {
    "block_id": "0404cd00-c88f-4c3e-981d-decc7e8e79c2",
    "feature_id": "0d4eae7e-bf51-e61f-7186-f7780924a8cb"
  }
]
```

---

#### `GET /features/getPinData` => Get data related to a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false | | String |

***Python example***
```
import urllib2

def get_pin_data():
    base_url = 'https://api2.terravion.com/'
    method = 'features/getPinData'
    feature_id = 'YOUR_FEATURE_ID'
    access_token = 'YOUR_ACCESS_TOKEN'
    url = base_url + method
    url += '?featureId=' + feature_id
    url += '&access_token=' + access_token
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

get_pin_data()
```

***Sample Response***
```
[
  {
    "feature_id": "0d4eae7e-bf51-e61f-7186-f7780924a8cb",
    "meta": {
      "title": "IDC",
      "text": ""
    },
    "add_date": "2019-09-12T00:21:13.285Z",
    "creator_user_id":
     "1bab6d1e-43ce-4574-8ec4-2708899cd2c6",
    "first_name": "Joe",
    "last_name": "Doe",
    "st_asgeojson": "{\"type\":\"Point\",\"coordinates\":[-100.60236709429,37.6356264849986]}",
    "block_id": "0404cd00-c88f-4c3e-981d-decc7e8e79c2"
  }
]
```
---

#### `GET /features/{featureId}/thumb.jpg` => Get image related to a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false |  | String |

***Python example***
```
import urllib2

def get_pin_image():
    base_url = 'https://api2.terravion.com/'
    feature_id = 'YOUR_FEATURE_ID'
    method = 'features/' + feature_id + '/thumb.jpg'
    access_token = 'YOUR_ACCESS_TOKEN'
    url = base_url + method
    url += '?access_token=' + access_token
    response = urllib2.urlopen(url)
    img = response.read()
    return img

get_pin_image()
```

***Sample response***
```
YOU WOULD GET A JPG IMAGE
```

---
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
***Python example***
```
import urllib
import urllib2
import json
import uuid

def store_pin():
    base_url = 'https://api2.terravion.com/'
    method = 'features/storePin'
    user_id = 'YOUR_USER_ID'
    access_token = 'YOUR_ACCESS_TOKEN'
    uuid = str(uuid.uuid4())

    url = base_url + method
    url += '?access_token=' + access_token

    # create a Python data object (dict):
    data = {
      "meta": {
        title,
        text
      },
      "imageMeta": {
        "origURL": "DEVICE_LOCAL_PATH",
        "url": "CLOUD_URL_IF_ANY"
      },
      "st_asgeojson": {
        "type": "Point",
        "coordinates": [ longitude, latitude ]
      },
      "block_id": "YOUR_BLOCK_ID",
      "feature_id": uuid,
      "userId": "YOUR_USER_ID",
      "add_date": "2018-10-14T15:19:31.073Z"
    }
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req).read()

    return response

store_pin()
```
***Response***
```
Simple 200 response
```
---

#### `POST /features/storePinImage` => Store image for Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| data | false | formData | String |

***Sample formData***
```
{
  uri: base64_encoded_image,
  name
}
```
***Python example***
```
import urllib
import urllib2
import json
import uuid

def store_pin_image():
    base_url = 'https://api2.terravion.com/'
    method = 'features/storePinImage'
    user_id = 'YOUR_USER_ID'
    access_token = 'YOUR_ACCESS_TOKEN'
    image_name = 'YOUR_FEATURE_ID' + '.jpg'

    url = base_url + method
    url += '?access_token=' + access_token

    # create a Python data object (dict):
    data = {
      "uri": "YOUR_BASE64_IMG",
      "name": image_name
    }
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req).read()

    return response

store_pin_image()
```
***Response***
```
Simple 200 response
```
---

#### `GET /features/deletePin` => Delete a single Pin

| Parameter| Required | Description | Type |
| - | - | - | - |
| featureId | false |  | String |

***Python example***
```
import urllib2

def delete_pin():
    base_url = 'https://api2.terravion.com/'
    method = 'features/deletePin'
    feature_id = 'YOUR_FEATURE_ID'
    access_token = 'YOUR_ACCESS_TOKEN'
    url = base_url + method
    url += '?feature_id=' + feature_id
    url += '?access_token=' + access_token
    response = urllib2.urlopen(url)
    img = response.read()
    return img

delete_pin()
```
***Response***
```
Simple 200 response
```