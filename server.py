from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from model import User, Playlist, connect_to_db, db

import os

import requests



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['AccuWeather_Key']

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
    print zipcode
    print "---------"
    payload = {'apikey': app.secret_key,
                'q': zipcode, 'language': 'en-us'}

    weather = requests.get('http://dataservice.accuweather.com/locations/v1/postalcodes/search',
                            params=payload)

    weather_list = weather.json()

    zipcode_key = weather_list[0]['Key']

    # print zipcode_key
    # return zipcode_key






























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
