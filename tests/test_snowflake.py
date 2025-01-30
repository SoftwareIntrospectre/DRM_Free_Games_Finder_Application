import unittest
from snowflake.snowflake_config import get_snowflake_connection
from snowflake.sql_queries import insert_steam_game, insert_gog_game

class TestSnowflakeIntegration(unittest.TestCase):

    @patch('snowflake.snowflake_config.snowflake.connector.connect')  # Mock Snowflake connection
    def test_insert_steam_game(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.return_value = None  # Mocking successful insert

        steam_game = {'steam_game_id': 12345, 'steam_game_name': 'Test Steam Game', 'price': 19.99}
        result = insert_steam_game(steam_game)
        mock_cursor.execute.assert_called_once_with("INSERT INTO steam_games (...) VALUES (%s, %s, %s)", (12345, 'Test Steam Game', 19.99))
        self.assertTrue(result)  # Ensure the insert returns True

    @patch('snowflake.snowflake_config.snowflake.connector.connect')  # Mock Snowflake connection
    def test_insert_gog_game(self, mock_connect):
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.return_value = None  # Mocking successful insert

        gog_game = {'gog_game_id': 101, 'gog_game_name': 'Test GOG Game', 'price': 9.99}
        result = insert_gog_game(gog_game)
        mock_cursor.execute.assert_called_once_with("INSERT INTO gog_games (...) VALUES (%s, %s, %s)", (101, 'Test GOG Game', 9.99))
        self.assertTrue(result)  # Ensure the insert returns True

if __name__ == "__main__":
    unittest.main()
