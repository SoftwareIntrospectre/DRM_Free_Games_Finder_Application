import pytest
from data_pipeline.steam_api import get_steam_game_list

def test_get_steam_game_list():
    data = get_steam_game_list()
    assert isinstance(data, dict)  # Assuming response is a dict
    assert 'applist' in data
