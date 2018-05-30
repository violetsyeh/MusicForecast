from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from model import User, Playlist, connect_to_db, db
import spotipy
import os
import requests
import spotipy.oauth2 as oauth2
import spotipy.util as util
from config import AccuWather_API_Key, Spotify_Client_Id, Spotify_Client_Secret, Redirect_Uri, SCOPE, CACHE

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

sp_oauth = oauth2.SpotifyOAuth(client_id=Spotify_Client_Id, client_secret=Spotify_Client_Secret,
                                redirect_uri=Redirect_Uri,scope=SCOPE, cache_path=CACHE)
auth_url = sp_oauth.get_authorize_url()

@app.route('/')
def index():
    """Homepage."""

    # access_token = ""
    token_info = sp_oauth.get_cached_token()
    #
    # if token_info:
    #     # print "cached_token found"
    #     # print '========='
    #     access_token = token_info['access_token']
    #
    #     # if credentials.is_token_expired(token_info):
    #     #     refresh_access_token()
    # # else:
    #     sp = spotipy.Spotify(auth=access_token)
    #     user = sp.current_user()
    #     return render_template('homepage.html', user=user, auth_url=auth_url)
    #
    # else:
    #     url = request.url
    #     code = sp_oauth.parse_response_code(url)
    #     # print code
    #     # print '====================code'
    #
    #     if code:
    #         # print "found spotify auth code in request url"
    #         token_info = sp_oauth.get_access_token(code)
    #         access_token = token_info['access_token']
    if token_info:
        get_sp_access_token()
        return render_template("homepage.html", auth_url=auth_url)
    # if access_token:
    else:
        return redirect('/login')


@app.route('/login')
def login():
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    url = request.url
    code = sp_oauth.parse_response_code(url)

    # print code
    # print '===================='

    if code:
        # print "found spotify auth code in request url"
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']

    if access_token:
        # print "access token exists"
        # sp = spotipy.Spotify(access_token)
        # user = sp.current_user()
        # user_id = user['id']
        sp = spotipy.Spotify(access_token)
        add_user_to_session(access_token)
        return redirect('/show-featured-playlists')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have sucessfully logged out.')
    return render_template("homepage.html", auth_url=auth_url)



@app.route('/weather-playlist-lookup', methods=['GET'])
def display_playlists():
    """Look up location key by zipcode"""

    zipcode = request.args.get("zipcode")

    payload = {'apikey': AccuWather_API_Key, 'q': zipcode, 'language': 'en-us'}

    location = requests.get('http://dataservice.accuweather.com/locations/v1/postalcodes/search',
                            params=payload)

    location_list = location.json()

    if location_list == []:
        flash("Please enter a valid zipcode.")
        return redirect('/')

    else:
        zipcode_key = location_list[0]['Key']
        weather_condition = lookup_weather_condition(zipcode_key).lower()
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

@app.route('/show-featured-playlists', methods=['GET'])
def show_featured_playlists():
    sp = get_sp_access_token()
    limit = 8
    results = sp.featured_playlists(locale=None, country=None, timestamp=None, limit=limit, offset=0)
    if results:
        playlists = []
        i = 0

        for i in range(limit):
            playlists.append(results['playlists']['items'][i]['uri'])
        return render_template('show-featured-playlists.html', playlists=playlists)

##################################################################################################
"""Helper functions"""

def lookup_zipcode_key():

    zipcode = request.args.get("zipcode")

    payload = {'apikey': AccuWather_API_Key, 'q': zipcode, 'language': 'en-us'}

    location = requests.get('http://dataservice.accuweather.com/locations/v1/postalcodes/search',
                            params=payload)

    location_list = location.json()

    return location_list

def lookup_weather_condition(zipcode_key):
    """Look up weather condition by location key"""

    payload = {'apikey': AccuWather_API_Key}

    weather = requests.get('http://dataservice.accuweather.com/currentconditions/v1/%s' % zipcode_key,
                            params=payload)

    weather_list = weather.json()

    weather_text = weather_list[0]['WeatherText']

    return weather_text

def authenticate_spotify():
    """Authenticate spotify with credentials for token without login"""

    credentials = oauth2.SpotifyClientCredentials(client_id=Spotify_Client_Id,
                                                client_secret=Spotify_Client_Secret)
    token = credentials.get_access_token()

    spotify = spotipy.Spotify(auth=token)
    return spotify

# def refresh_access_token():
#     if sp_oauth.is_token_expired(token_info):
#         token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
#         token = token_info['access_token']
#         sp = spotipy.Spotify(auth=token)

def get_sp_access_token():
    access_token = ""
    token_info = sp_oauth.get_cached_token()

    if token_info:
        # print "cached_token found"
        # print '========='
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)
        return sp
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        # print code
        # print '====================code'

        if code:
            # print "found spotify auth code in request url"
            sp = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
            return sp


def add_user_to_session(access_token):
    sp = spotipy.Spotify(access_token)
    user = sp.current_user()
    user_id = user['id']
    session['current_user'] = user_id


# def add_user_to_db():





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
