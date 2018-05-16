from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from model import User, Playlist, connect_to_db, db
import os
import spotipy
import requests
import spotipy.oauth2 as oauth2

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.AccuWather_API_Key = os.environ['AccuWeather_Key']
app.Spotify_Client_Id = os.environ['Spotify_Client_Id']
app.Spotify_Client_Secret = os.environ['Spotify_Client_Secret']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/weather-playlist-lookup', methods=['GET'])
def display_playlists():
    """Look up location key by zipcode"""

    zipcode = request.args.get("zipcode")

    payload = {'apikey': app.AccuWather_API_Key, 'q': zipcode, 'language': 'en-us'}

    location = requests.get('http://dataservice.accuweather.com/locations/v1/postalcodes/search',
                            params=payload)

    location_list = location.json()

    if location_list == []:
        flash("Please enter a valid zipcode.")
        return redirect('/')

    else:
        zipcode_key = location_list[0]['Key']
        weather_condition = lookup_weather_condition(zipcode_key)
        return lookup_playlists(weather_condition)

def lookup_playlists(weather_condition):
    """Look up playlists related to weather condition"""

    limit = 8
    spotify = authenticate_spotify()
    results = spotify.search(q=weather_condition, type='playlist', market='US', limit=limit, offset=0)

    if results:
        playlists = []
        i = 0

        for i in range(limit):
            playlists.append(results['playlists']['items'][i]['uri'])
        return render_template("show-playlists.html", playlists=playlists, weather_condition=weather_condition)
    else:
        flash('Sorry we were not able to find any playlists based on the forecast.')
        return redirect('/')

@app.route('/sunny-playlists', methods=['GET'])
def display_sunny_playlists():
    """Display sunny playlists without weather lookup"""

    weather_condition = 'sunny'
    return lookup_playlists(weather_condition)

@app.route('/cloudy-playlists', methods=['GET'])
def display_cloudy_playlists():
    """Display cloudy playlists without weather lookup"""

    weather_condition = 'cloudy'
    return lookup_playlists(weather_condition)

@app.route('/rainy-playlists', methods=['GET'])
def display_rainy_playlists():
    """Display cloudy playlists without weather lookup"""

    weather_condition = 'rainy'
    return lookup_playlists(weather_condition)

##################################################################################################
"""Helper functions"""
def lookup_zipcode_key():

    zipcode = request.args.get("zipcode")

    payload = {'apikey': app.AccuWather_API_Key, 'q': zipcode, 'language': 'en-us'}

    location = requests.get('http://dataservice.accuweather.com/locations/v1/postalcodes/search',
                            params=payload)

    location_list = location.json()

    return location_list

def lookup_weather_condition(zipcode_key):
    """Look up weather condition by location key"""

    payload = {'apikey': app.AccuWather_API_Key}

    weather = requests.get('http://dataservice.accuweather.com/currentconditions/v1/%s' % zipcode_key,
                            params=payload)

    weather_list = weather.json()

    weather_text = weather_list[0]['WeatherText']

    return weather_text

def authenticate_spotify():
    """Authenticate spotify with credentials for token"""

    credentials = oauth2.SpotifyClientCredentials(client_id=app.Spotify_Client_Id,
                                                client_secret=app.Spotify_Client_Secret)
    token = credentials.get_access_token()

    spotify = spotipy.Spotify(auth=token)
    return spotify









if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=5000, host='0.0.0.0')
