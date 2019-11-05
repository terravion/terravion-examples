'use strict';
require('dotenv').config()

'use strict';

const app = require('express')();
const port = 3000;

const TOKEN_HOST = 'https://maps.terravion.com'
const TOKEN_PATH = '/oauth2/token'
const AUTH_PATH = '/oauth2/authorize'
const CALLBACK_URL = `http://localhost:${port}/callback`;

const credentials = {
  client: {
    id: process.env.CLIENT_ID,
    secret: process.env.CLIENT_SECRET,
  },
  auth: {
    tokenHost: TOKEN_HOST,
    tokenPath: TOKEN_PATH,
    authorizePath: AUTH_PATH,
  },
  options: {
    authorizationMethod: 'body',
  }
};

// Initialize the OAuth2 Library
const oauth2 = require('simple-oauth2').create(credentials);

// Authorization uri definition
const authorizationUri = oauth2.authorizationCode.authorizeURL({
  redirect_uri: CALLBACK_URL,
});

// Initial page redirecting to TerrAvion
app.get('/auth', (req, res) => {
  console.log(authorizationUri);
  res.redirect(authorizationUri);
});

// Callback service parsing the authorization token and asking for the access token
app.get('/callback', async (req, res) => {
  const code = req.query.code;
  const options = {
    code,
  };

  try {
    const result = await oauth2.authorizationCode.getToken(options);
    console.log('The resulting token: ', result);
    const token = oauth2.accessToken.create(result);
    return res.status(200).json(token)
  } catch(error) {
    console.error('Access Token Error', error.message);
    return res.status(500).json('Authentication failed');
  }
});

// Starting point front end interface
app.get('/', (req, res) => {
  res.send('Hello<br><a href="/auth">Log in with TerrAvion</a>');
});

app.listen(port, (err) => {
  if (err) return console.error(err);
  console.log(`Express server listening at http://localhost:${port}`);
});