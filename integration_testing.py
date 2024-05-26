import unittest
from flask import Flask
from flask.testing import FlaskClient
from recommendation_api import song_recommender, artist_recommender
from recommendation_api import app

import warnings

class RecommendationSystemTestCase(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        self.app = app.test_client()
        self.app.testing = True

    def test_get_recommended_songs_valid(self):
        response = self.app.get('/get-recommended-songs?song_name=Blinding Lights')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn('name', data[0])
        self.assertIn('artists', data[0])
        self.assertIn('release_year', data[0])

    def test_get_recommended_songs_invalid(self):
        response = self.app.get('/get-recommended-songs?song_name=Nonexistent Song Name')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_recommended_songs_no_param(self):
        response = self.app.get('/get-recommended-songs')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_recommended_artists_valid(self):
        response = self.app.get('/get-recommended-artists?artist_name=Taylor Swift')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn('name', data[0])
        self.assertIn('genres', data[0])
        self.assertIn('followers', data[0])
        self.assertIn('popularity', data[0])

    def test_get_recommended_artists_invalid(self):
        response = self.app.get('/get-recommended-artists?artist_name=Nonexistent Artist Name')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_recommended_artists_no_param(self):
        response = self.app.get('/get-recommended-artists')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
