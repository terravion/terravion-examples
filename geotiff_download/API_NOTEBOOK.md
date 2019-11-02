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

## Bulk Download Geotiffs

> This call allows you to request all the geotiffs for your layers on a given time range.  
> As a result it will generate a task_id which will allow you to access your download once ready.

### ENDPOINT

`POST /tasks/requestGeotiffTaskBulkRequest`

### OPTIONS

| Parameter | Required | Format | Data Type |
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
