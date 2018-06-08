import os

AccuWather_API_Key = os.environ['AccuWeather_Key']
Spotify_Client_Id = os.environ['Spotify_Client_Id']
Spotify_Client_Secret = os.environ['Spotify_Client_Secret']
Redirect_Uri = 'http://0.0.0.0:5000/login'
SCOPE = 'playlist-modify-public playlist-modify-private'
CACHE = '.spotipyoauthcache'
logout_url = 'https://www.spotify.com/us/logout/'
