import unittest
from recommendation_system import song_recommender, artist_recommender
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

class TestRecommendationSystem(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)

    def test_song_recommender_existing_song(self):
        result = song_recommender("Blinding Lights")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_song_recommender_non_existing_song(self):
        result = song_recommender("Non-existing Song Name")
        self.assertIsNone(result)

    def test_artist_recommender_existing_artist(self):
        result = artist_recommender("Taylor Swift")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_artist_recommender_non_existing_artist(self):
        result = artist_recommender("Non-existing Artist Name")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()