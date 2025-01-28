from fastapi import APIRouter
from app.models import Game
from typing import List

game_router = APIRouter()

# Sample route for searching a game on Steam
@game_router.get("/game/{game_name}", response_model=Game)
def get_game(game_name: str):
    # Placeholder logic to query the database or external APIs
    game = {
        "name": game_name,
        "on_steam": True,
        "on_gog": False
    }
    return game