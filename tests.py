from server import app
import server
import unittest
from unittest import TestCase
import os
from flask import Flask
from model import db, connect_to_db


class FlaskTests(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):

        result = self.client.get('/')
        self.assertIn('<h2>Enter your zipcode here:</h2>', result.data)

    def test




















if __name__ == "__main__":
    unittest.main()
