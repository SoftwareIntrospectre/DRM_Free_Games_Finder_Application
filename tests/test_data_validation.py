import unittest
from data_validation import validate_steam_data, validate_gog_data

class TestDataValidation(unittest.TestCase):

    def test_validate_steam_data(self):
        valid_data = {'steam_game_id': 12345, 'steam_game_name': 'Test Steam Game', 'price': 19.99, 'release_date': '2020-01-01'}
        invalid_data = {'steam_game_id': 12345, 'steam_game_name': '', 'price': 'not-a-number', 'release_date': 'invalid-date'}

        self.assertTrue(validate_steam_data(valid_data))  # Should pass validation
        self.assertFalse(validate_steam_data(invalid_data))  # Should fail validation

    def test_validate_gog_data(self):
        valid_data = {'gog_game_id': 101, 'gog_game_name': 'Test GOG Game', 'price': 9.99, 'release_date': '2021-02-01'}
        invalid_data = {'gog_game_id': 101, 'gog_game_name': '', 'price': 'not-a-number', 'release_date': 'invalid-date'}

        self.assertTrue(validate_gog_data(valid_data))  # Should pass validation
        self.assertFalse(validate_gog_data(invalid_data))  # Should fail validation

if __name__ == "__main__":
    unittest.main()
