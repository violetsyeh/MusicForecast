from server import app
import server
import unittest
from unittest import TestCase
import os
from flask import Flask
from model import db, connect_to_db

app.AccuWather_API_Key = os.environ['AccuWeather_Key']

class FlaskTests(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):

        result = self.client.get('/')
        self.assertIn('<h2>Enter your zipcode here:</h2>', result.data)

class FlaskRouteTests(unittest.TestCase):

    def setUp(self):

        self.client = server.app.test_client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        Spotify_Client_Id = os.environ['Spotify_Client_Id']
        Spotify_Client_Secret = os.environ['Spotify_Client_Secret']


    def test_zipcode_to_key(self):

        result = self.client.get('/weather-lookup')























if __name__ == "__main__":
    unittest.main()
