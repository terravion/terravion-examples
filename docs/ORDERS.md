## Working with Orders
> There are various methods to work with orders.  
> Here we only show you a single endpoint example.

### ENDPOINTS

`GET /layers/getOrderList`

### OPTIONS

| Parameter| Required | Description | Type |
| - | - | - | - |
| userId | false | | String |
| distributorId | false | | String |
| orderDateEpochEnd | false | | Double |

### EXAMPLE

```
curl -X POST --header "Accept: application/json" "https://api2.terravion.com/orders/getOrderList?\
userId=YOUR_USER_ID\
&access_token=YOUR_ACCESS_TOKEN"
```

### RESULT

```
[
  "a3ad5ba7-2e9f-4ef5-b676-9be00f4aaec9",
  "bdce472c-549e-44cf-899e-6896d1ddb353",
  "4a330d11-da1f-4712-8012-9c98f58f9fc8"
]
```