## Intro

To start using the API, you will need 3 things:
1. An **Activated** TerrAvion user account 
2. The access token for the account
3. Images, field names, or other data in the account

---
## Assumptions

In these docs we make the following assumptions:

1. You know how to use the comand line tools on your computer.
2. You are familiar with javascript and/ or python.
3. You have a basic knowledge of how an api works.

---
## Getting a TerrAvion account

There are several ways to get a TerrAvion account:
1. You can sign up for a new account [here](https://maps.terravion.com/signup) or view instructions [here](https://help.terravion.com/how-to-create-an-account-with-terravion).
2. If you are setting up the API for a co-worker or client, they can [share imagery](https://help.terravion.com/how-to-share-my-terravion) with your email address, and this will create an account.

You will need to authenticate your account before you can log in or start using the API. You will receive an email, and you'll need to click a link and set a password.

Make sure you have the ability to check messages for whichever email address you use.

---
## Getting an access token

When using our api you will need authorization to get information from a user's account. This authorization is called an _access token_. Each user has a unique acess token for their account. 

### A. Get your own accessToken:

An access token can be obtained by authenticating via [Oauth2](https://oauth.net/2/). 

We have an [instructional video](https://www.youtube.com/watch?v=-Ur1WI4Iaj0) which shows how to authenticate using the [postman](https://www.getpostman.com/) client.

You will need a _client ID_ and _client secret_ which can be obtained by visiting the [developer apps](https://maps.terravion.com/settings/developer-apps) section of the settings page in your account, clicking _register new application_, then providing an Application name and [callback URL](https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2).

You can use the following API calls for authentication
**Oauth2 Authorize endpoint**: https://maps.terravion.com/oauth2/authorize
**Oauth2 Token endpoint**: https://maps.terravion.com/oauth2/token

Following the instructional video will give you the access token for the account you used.

### B. Using our demo accessToken

If you just want to test the API you can get started using our demo accessToken

```
03uKC6WwDrVUfh4jFrANmEMUegXApJXTeEYrGQc9Rf1ViWtByZEIMQ43CIepS7Cg
```

---
## Getting sample fields or data into your account

The simplest way to get sample data into your account is to have an existing user [share imagery](https://help.terravion.com/how-to-share-my-terravion) with you. This could be a co-worker, a client, or even one of our salespeople.

If you're building a new API connection and do not have any sample imagery, a sales representative can share some data with you: email sales@terravion.com

## Other Basic functionality: Getting your User ID

Each email address in our system has a User ID. We use [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)s and these IDs are required for many api calls.

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
## Looking up field (block) information by name

`GET /userBlocks/getBlocksByName`

**EXAMPLE**
```
curl -X GET --header "Accept: application/json" "https://api2.terravion.com/userBlocks/getBlocksByName?\
userId=YOUR_USER_ID\
blockName=YOUR_BLOCK_NAME\
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




---

## FAQ

**Q:** Should I have one master account connect to the TerrAvion app--or should I allow users to make their own connections?

**A:** In most cases you'll want to allow users to make their own connection: for security purposes when you're using             our tile API, if they're going to report image issues through our APP, or any time they're going to purchase their own image             subscription.

**Q:** What if I just need to use the API one time to do a bulk data export? Can you help me with the API connection? Can you connect to my app's API?

**A:** We offer custom engineering services--reach out to support@terravion.com to start a discussion.
