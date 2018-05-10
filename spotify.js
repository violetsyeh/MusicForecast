import os

var request = require('request'); // "Request" library

var client_id = os.environ['Spotify_Client_Id']; // Your client id
var client_secret = os.environ['Spotify_Client_Secret']; // Your secret

// your application requests authorization
var authOptions = {
  url: 'https://accounts.spotify.com/api/token',
  headers: {
    'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
  },
  form: {
    grant_type: 'client_credentials'
  },
  json: true
};

request.post(authOptions, function(error, response, body) {
  if (!error && response.statusCode === 200) {

    // use the access token to access the Spotify Web API
    var token = body.access_token;
    var options = {
      url: 'https://api.spotify.com/v1/search?q=sunny&type=playlist&market=US&limit=6&offset=0',
      headers: {
        'Authorization': 'Bearer ' + token
      },
      json: true
    };
    request.get(options, function(error, response, body) {
      // console.log(body)
      // console.log(body["playlists"]["items"])
      console.log(body["playlists"]["items"][0]["uri"])
    });
  }
});
