from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from model import User, Playlist, connect_to_db, db
import spotipy
import os
import requests
import time
import spotipy.oauth2 as oauth2
import spotipy.util as util
from config import AccuWather_API_Key, Spotify_Client_Id, Spotify_Client_Secret, Redirect_Uri, SCOPE, CACHE, logout_url

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
    return render_template("homepage.html", auth_url=auth_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    token_info = sp_oauth.get_cached_token()
    # if token_info:
    #     # flash('You are already logged in')
    #
    #     return redirect('/show-featured-playlists')
    # else:
    access_token = get_sp_access_token()
    print access_token
    if access_token:
        add_user_to_session(access_token)
        flash('You have sucessfully logged in.')
        return redirect('/show-featured-playlists')
    else:
        flash('Your Spotify Account was unable to be verified.')
    return redirect('/show-featured-playlists')

@app.route('/logout')
def logout():

    session.clear()
    return redirect('/')


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

    limit = 9
    spotify = authenticate_spotify()

    results = spotify.search(q=weather_condition, type='playlist', market='US', limit=limit, offset=0)

    if results:
        playlists = []
        i = 0

        for i in range(limit):
            playlists.append((results['playlists']['items'][i]['uri'], results['playlists']['items'][i]['owner']['id'],
                            results['playlists']['items'][i]['id']))
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
    spotify = authenticate_spotify()
    limit = 9
    results = spotify.featured_playlists(locale=None, country=None, timestamp=None, limit=limit, offset=0)
    if results:
        playlists = []
        i = 0

        for i in range(limit):
            playlists.append((results['playlists']['items'][i]['uri'], results['playlists']['items'][i]['owner']['id'],
                            results['playlists']['items'][i]['id']))
        return render_template('show-featured-playlists.html', playlists=playlists)
    else:
        flash('Unable to display featured playlists right now.')
        return redirect('/')

@app.route('/follow-playlist/', methods=['GET','POST'])
def follow_playlist():
    access_token = get_sp_access_token()
    sp = spotipy.Spotify(auth=access_token)

    playlist_owner_id = request.form.get("playlist_owner_id")
    # print playlist_owner_id
    # print 'playlist_owner_id form'
    playlist_id = request.form.get("playlist_id")
    # print playlist_id
    # print 'playlist_id form'
    user = sp.current_user()
    user_id = user['id']
    response = sp.user_playlist_is_following(playlist_owner_id=playlist_owner_id, playlist_id=playlist_id, user_ids=[user_id])
    # print response
    if response == [True]:
        flash('You are already following that playlist.')
        redirect('/current-followed-playlists')
    else:
        sp.user_playlist_follow_playlist(playlist_owner_id=playlist_owner_id,
                            playlist_id=playlist_id)
    return redirect('/current-followed-playlists')

@app.route('/current-followed-playlists', methods=['GET'])
def show_followed_playlists():
    access_token = get_sp_access_token()
    sp = spotipy.Spotify(auth=access_token)
    user = sp.current_user()
    user_id = user['id']
    limit = 20
    results = sp.user_playlists(user=user_id, limit=limit, offset=0)
    playlist_len = results['total']
    # print playlist_len
    # print '=============='
    if results:
        playlists = []
        i = 0

        for i in range(playlist_len):
            playlists.append(results['items'][i]['uri'])
        return render_template('current-followed-playlists.html', playlists=playlists)
    else:
        flash('You do not follow any playlists currently.')
        return redirect('/')

@app.route('/refresh-token')
def refresh():
    token_info = sp_oauth.get_cached_token()
    # access_token = get_sp_access_token()
    # print access_token
    # print '=============0---------------'
    # # sp = spotipy.Spotify(auth=access_token)
    expired_result = is_token_expired(token_info)
    if expired_result:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        print token_info
        print '================='
        token = token_info['access_token']
        # sp = spotipy.Spotify(auth=token)
        return token
    return 'token still valid'
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

def get_sp_access_token():
    access_token = ""
    token_info = sp_oauth.get_cached_token()
    # print token_info

    if token_info:
        access_token = token_info['access_token']
        refresh_token = token_info['refresh_token']
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        sp = spotipy.Spotify(auth=access_token)
        return access_token
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)

        if code:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
            refresh_token = token_info['refresh_token']
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token
            return access_token

def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60

def add_user_to_session(access_token):
    sp = spotipy.Spotify(access_token)
    user = sp.current_user()
    spotify_user_id = user['id']
    find_user = User.query.filter(User.spotify_user_id == spotify_user_id).first()
    print find_user
    if find_user:
        print 'User already in database'
    else:
        session['current_user'] = spotify_user_id
        spotify_user = User(spotify_user_id=spotify_user_id, access_token= access_token)
        db.session.add(spotify_user)
        db.session.commit()
    print "spotify_user added successfully"






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
