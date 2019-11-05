## What you need:

### 1. An access token and userId

1. you can start using our api@terravion.com token

```
03uKC6WwDrVUfh4jFrANmEMUegXApJXTeEYrGQc9Rf1ViWtByZEIMQ43CIepS7Cg
```
        
2. you can ask for your own token to api@terravion.com

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