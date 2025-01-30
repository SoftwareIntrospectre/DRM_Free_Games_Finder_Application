import unittest
from fastapi.testclient import TestClient
from app.main import app  # Assuming main.py contains the FastAPI app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)  # Initialize the FastAPI test client

    # Test GET all games from both Steam and GOG
    def test_get_games(self):
        # Test retrieving all games from Steam
        response = self.client.get("/api/games/steam")  # Endpoint for Steam games
        self.assertEqual(response.status_code, 200)
        self.assertIn("games", response.json())

        # Test retrieving all games from GOG
        response = self.client.get("/api/games/gog")  # Endpoint for GOG games
        self.assertEqual(response.status_code, 200)
        self.assertIn("games", response.json())

    # Test GET a single game by ID for both Steam and GOG
    def test_get_game_by_id(self):
        game_id = 1  # Replace with a valid game ID for Steam
        response = self.client.get(f"/api/games/steam/{game_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json())  # Ensure the game name is present

        game_id = 101  # Replace with a valid game ID for GOG
        response = self.client.get(f"/api/games/gog/{game_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json())  # Ensure the game name is present

    # Test POST game data for both Steam and GOG
    def test_post_game_data(self):
        # Example game data for Steam
        steam_game_data = {
            "steam_game_id": 123,
            "steam_game_name": "Steam Test Game",
            "price": 19.99,
            "developer": "Steam Developer",
            "release_date": "Jan 1, 2020"
        }
        response = self.client.post("/api/games/steam", json=steam_game_data)
        self.assertEqual(response.status_code, 201)  # Assuming 201 is returned for successful post

        # Example game data for GOG
        gog_game_data = {
            "gog_game_id": 101,
            "gog_game_name": "GOG Test Game",
            "price": 9.99,
            "developer": "GOG Developer",
            "release_date": "Feb 1, 2021"
        }
        response = self.client.post("/api/games/gog", json=gog_game_data)
        self.assertEqual(response.status_code, 201)  # Assuming 201 is returned for successful post

    # Test invalid POST game data for both Steam and GOG
    def test_invalid_post_game(self):
        # Invalid Steam game data (missing name and invalid price)
        invalid_steam_data = {
            "steam_game_name": "",
            "price": "not-a-number"
        }
        response = self.client.post("/api/games/steam", json=invalid_steam_data)
        self.assertEqual(response.status_code, 400)  # Bad request due to validation errors

        # Invalid GOG game data (missing name and invalid price)
        invalid_gog_data = {
            "gog_game_name": "",
            "price": "not-a-number"
        }
        response = self.client.post("/api/games/gog", json=invalid_gog_data)
        self.assertEqual(response.status_code, 400)  # Bad request due to validation errors

if __name__ == "__main__":
    unittest.main()
