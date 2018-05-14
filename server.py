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

@app.route('/weather-lookup', methods=['GET'])
def lookup_location_key():
    """Look up location key by zipcode"""

    zipcode = request.args.get("zipcode")
    # print zipcode
    # print "---------"
    payload = {'apikey': app.AccuWather_API_Key, 'q': zipcode, 'language': 'en-us'}

    # location = requests.get('http://dataservice.accuweather.com/locations/v1/postalcodes/search',
    #                         params=payload)

    # location_list = location.json()

    # zipcode_key = location_list[0]['Key']


    # weather_condition = lookup_weather_condition(zipcode_key)
    weather_condition = 'sunny'
    # print zipcode_key
    # print weather_condition
    # return render_template("show-playlists.html", weather_condition=weather_condition)
    return show_playlists(weather_condition)

# def lookup_weather_condition(zipcode_key):
#     """Look up weather condition by location key"""
#
#     payload = {'apikey': app.AccuWather_API_Key}
#
#     weather = requests.get('http://dataservice.accuweather.com/currentconditions/v1/%s' % zipcode_key,
#                             params=payload)
#
#     weather_list = weather.json()
#
#     weather_text = weather_list[0]['WeatherText']
#
#     return weather_text

def show_playlists(weather_condition):
    """Look up playlists related to weather condition"""

    credentials = oauth2.SpotifyClientCredentials(client_id=app.Spotify_Client_Id,
                                                client_secret=app.Spotify_Client_Secret)
    print weather_condition
    token = credentials.get_access_token()

    spotify = spotipy.Spotify(auth=token)
    results = spotify.search(q=weather_condition, type='playlist', market='US', limit=6,offset=0)

    playlists = []
    i = 0

    for i in range(0,6):
        playlists.append(results['playlists']['items'][i]['uri'])
        i += 1
    print playlists
    return render_template("show-playlists.html", playlists=playlists)



















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
