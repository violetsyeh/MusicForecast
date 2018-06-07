from server import app
import server
import unittest
from unittest import TestCase
import os
from flask import Flask
from model import db, connect_to_db
import json

AccuWather_API_Key = os.environ['AccuWeather_Key']
Spotify_Client_Id = os.environ['Spotify_Client_Id']
Spotify_Client_Secret = os.environ['Spotify_Client_Secret']

class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_sunny_dropdown(self):

        result = self.client.get('/sunny-playlists')
        self.assertIn('<h1>Your sunny playlists for today: </h1>', result.data)
    def test_cloudy_dropdown(self):

        result = self.client.get('/cloudy-playlists')
        self.assertIn('<h1>Your cloudy playlists for today: </h1>', result.data)

    def test_rainy_dropdown(self):

        result = self.client.get('/rainy-playlists')
        self.assertIn('<h1>Your rainy playlists for today: </h1>', result.data)

    def test_show_featured_playlists(self):

        result = self.client.get('/show-featured-playlists')
        self.assertIn("<h2>Today's featured playlists:</h2>", result.data)

# class FlaskRouteTests(TestCase):
#
#     def setUp(self):
#
#         self.client = server.app.test_client()
#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
#         # Spotify_Client_Id = os.environ['Spotify_Client_Id']
#         # Spotify_Client_Secret = os.environ['Spotify_Client_Secret']
#
#     def test_incorrect_zipcode(self):
#
#         result = self.client.get('/weather-playlist-lookup', query_string={'zipcode':'jam'}, follow_redirects=True)
#         self.assertIn('Please enter a valid zipcode.',result.data)
#
#     def test_zipcode_to_key(self):
#         result = self.client.get('/weather-playlist-lookup', query_string={'zipcode':'94030'}, follow_redirects=True)
#         self.assertIsNot('Please enter a valid zipcode.', result.data)
#         self.assertIn('playlists for today:', result.data)
        # self.assertEqual(zipcode_key == '39346_PC')

# class HelperFunctionTests(TestCase):
#
#     def setUp(self):
#
#         # self.client = app.test_client()
#         app.config['TESTING'] = True
#
#     # def test_authenticate_spotify(self):
#     #
#     #     results = server.authenticate_spotify()
#     #     self.assertEqual(results == )
#
#     def test_lookup_weather_condition(self):
#
#         result = server.lookup_weather_condition('39346_PC')
#         print result
#         # self.assertEqual(result.weather == Response [200])


















if __name__ == "__main__":
    unittest.main()
