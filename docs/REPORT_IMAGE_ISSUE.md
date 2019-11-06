## Reporting image issue
> Sends an email to layer_issue@terravion.com about user reported issue.

### ENDPOINTS

`POST /layers/{layerId}/reportLayerIssue`

### OPTIONS

| Parameter| Required | Description | Type |
| - | - | - | - |
| layerId | true | | String |
| data | false | | String |

***data***
```
{
  "userId": "string",
  "description": "string",
}
```

### EXAMPLE

```
curl -X POST --header "Accept: application/json" -d "{
  \"description\": \"test\",
  \"userId\": \"7ct1da8c-b067-48e5-ab04-84fb6645409e\"
}" "https://api2.terravion.com/layers/YOUR_LAYER_ID/\
reportLayerIssue?access_token=YOUR_ACCESS_TOKEN"
```

### RESULT

```
204   Request was successful
```