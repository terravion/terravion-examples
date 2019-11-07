## What you need:

### 1. An access token and a User ID

- You can start by using our api@terravion.com token
- NOTE: Ask for your own access token by sending an email to api@terravion.com

```
03uKC6WwDrVUfh4jFrANmEMUegXApJXTeEYrGQc9Rf1ViWtByZEIMQ43CIepS7Cg
```

### 2. Get your User ID using from access token

#### EXAMPLE

```
curl -X GET --header "Accept: application/json" "https://api2.terravion.com/users/getUserId?access_token=YOUR_ACCESS_TOKEN"
```

#### RESULT

```
{
  "userId": "1455cf90-af48-4fae-87d0-57523de51b8b"
}
```