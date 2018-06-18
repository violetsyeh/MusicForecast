# MusicForecast
MusicForecast provides users a tool to find Spotify playlists based on the weather condition through the AccuWeather API. Through OAuth2 authorization, they are able to login into their own Spotify account to make modifications  and have access to playlists they currently follow. Users are able to view and follow playlists found through the weather condition and featured playlists of that day. Entire song playback is accessible when the user's account is verified, otherwise, 30 second playback is available.

## Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [Version 2.0](#version)
* [About Me](#aboutme)


## <a name="technologies"></a>Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: AccuWeather, Spotify<br/>

## <a name="features"></a>Features
![OAuth2](/static/images/readme/MusicForecastLogin.mov)

## <a name="install"></a>Installation

To run MusicForecast:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/violetsyeh/MusicForecast
```

Create and activate a virtual environment inside your Ride Thrift directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [AccuWeather API](https://developer.accuweather.com/) and the [Spotify API](https://developer.spotify.com/).

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export SECRET_KEY=="YOUR_KEY_HERE"
export AccuWeather_Key="YOUR_KEY_HERE"
export Spotify_Client_Id="YOUR_KEY_HERE"
export Spotify_Client_Secret="YOUR_KEY_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb weather
python model.py
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access MusicForecast.

## <a name="version"></a>Version 2.0
* Infinite scrolling
* Allow users to create playlists
* Create algorithm to suggest playlists to follow

## <a name="aboutme"></a>About Me
Violet Yeh is a Software Engineer in the Bay Area.
Learn more about Violet on [LinkedIn](http://www.linkedin.com/in/violetsyeh).
