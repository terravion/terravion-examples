## Intro

When interacting with our api you will need an authorization token on each request you make to the api, so as we know it is you the one asking for access to your resources. This is called an accessToken and it is binded to your userId.

Another thing that you will often need will be a userId. this is basically for the cases when you are doing a request on another users's behalf -for which you are authorized- and you need to specify which users you are asking this for.

In this document we will show you how to obtain your own accessToken and userId. And we also provide you a demo userId and accessToken should you only want to try things out.

---
## Assumptions

Throughout all our docs we'd do the following assumptions:

1. That you know how to use the comand line tools on your computer.
2. That you are familiar with javascript and/ or python.
3. That you have a basic knowledge on how an api works.

---
## How to get your access token

### A. Get your own accessToken:

To get your own accessToken write us to api@terravion.com specifying your username or the main account you need it for.

### B. Using our demo accessToken

Alternativeley, you can ge start using our demo accessToken

```
03uKC6WwDrVUfh4jFrANmEMUegXApJXTeEYrGQc9Rf1ViWtByZEIMQ43CIepS7Cg
```

---
## How to get a User ID

### A. With your own accessToken

**ENDPOINT**

`POST   /users/getUserId`

**EXAMPLE**
```
curl -X GET --header "Accept: application/json" "https://api2.terravion.com/users/getUserId?access_token=YOUR_ACCESS_TOKEN"
```

**RESULT**

```
{
  "userId": "1455cf90-af48-4fae-87d0-57523de51b8b"
}
```

### B. With our demo accessToken 

In this case, your `userId` would be:

```
1455cf90-af48-4fae-87d0-57523de51b8b
```
---
## How to get a Block by Name

`GET /userBlocks/getBlocksByName`

**EXAMPLE**
```
curl -X GET --header "Accept: application/json" "https://api2.terravion.com/userBlocks/getBlocksByName?\
userId=YOUR_USER_ID\
userId=YOUR_BLOCK_NAME\
access_token=YOUR_ACCESS_TOKEN"
``` 
**RESULT**
```
[
  {
    "blockId": "1f7141a9-7930-4715-9d60-d057fed6207d",
    "name": "Joe Doe/SW 34_23_24",
    "role": "OWNER"
  }
]
```