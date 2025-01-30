import unittest
from data_pipeline.steam_api import fetch_steam_data
from data_pipeline.gog_api import fetch_gog_data
from data_pipeline.spark_processing import process_data
from unittest.mock import patch

class TestDataPipeline(unittest.TestCase):

    @patch('data_pipeline.steam_api.requests.get')  # Mocking Steam API request
    def test_fetch_steam_data(self, mock_get):
        mock_get.return_value.json.return_value = {'applist': {'apps': [{'appid': 12345, 'name': 'Steam Test Game'}]}}
        result = fetch_steam_data()
        self.assertIsInstance(result, list)  # Ensure the result is a list of games
        self.assertEqual(len(result), 1)  # Check if one game is fetched
        self.assertEqual(result[0]['name'], 'Steam Test Game')

    @patch('data_pipeline.gog_api.requests.get')  # Mocking GOG API request
    def test_fetch_gog_data(self, mock_get):
        mock_get.return_value.json.return_value = {'games': [{'id': 101, 'name': 'GOG Test Game'}]}
        result = fetch_gog_data()
        self.assertIsInstance(result, list)  # Ensure the result is a list of games
        self.assertEqual(len(result), 1)  # Check if one game is fetched
        self.assertEqual(result[0]['name'], 'GOG Test Game')

    @patch('data_pipeline.spark_processing.SparkSession')  # Mocking Spark session
    def test_process_data(self, mock_spark):
        mock_spark.return_value.read.csv.return_value = [{'steam_game_id': 12345, 'steam_game_name': 'Test Game'}]
        result = process_data('mock_path')
        self.assertIsInstance(result, list)  # Ensure the processed data is a list
        self.assertGreater(len(result), 0)  # Ensure data is processed
        self.assertEqual(result[0]['steam_game_name'], 'Test Game')

if __name__ == "__main__":
    unittest.main()
