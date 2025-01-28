import pytest
from data_pipeline.data_validation import validate_game_data
from data_pipeline.spark_processing import process_game_data

# Sample valid and invalid game data
valid_game_data = [
    {
        "game_id": "1",
        "title": "Game A",
        "platform": "Steam",
        "price": 19.99,
        "is_drm_free": "Yes",
        "release_date": "2023-01-01",
        "game_status": "Steam and DRM-Free on GOG"
    },
    {
        "game_id": "2",
        "title": "Game B",
        "platform": "GOG",
        "price": 29.99,
        "is_drm_free": "Yes",
        "release_date": "2022-05-15",
        "game_status": "Exclusive to GOG"
    }
]

invalid_game_data = [
    {
        "game_id": "3",
        "title": None,  # Missing title
        "platform": "Steam",
        "price": 15.99,
        "is_drm_free": "No",
        "release_date": "2021-08-21",
        "game_status": "Steam"
    },
    {
        "game_id": "4",
        "title": "Game D",
        "platform": "GOG",
        "price": -5.00,  # Invalid price
        "is_drm_free": "Yes",
        "release_date": "2022-12-10",
        "game_status": "Exclusive to GOG"
    }
]

# Test the validation of the valid data
def test_validate_valid_game_data():
    for game in valid_game_data:
        result = validate_game_data(game)
        assert result == True, f"Validation failed for valid game data: {game}"

# Test the validation of invalid game data
def test_validate_invalid_game_data():
    for game in invalid_game_data:
        result = validate_game_data(game)
        assert result == False, f"Validation failed for invalid game data: {game}"

# Test the processing function (ensure it works with valid data)
def test_process_game_data_valid():
    processed_data = process_game_data(valid_game_data)
    assert len(processed_data) == 2, f"Processing failed for valid game data: {processed_data}"

# Test processing invalid data (should raise error or handle invalid cases)
def test_process_game_data_invalid():
    with pytest.raises(ValueError):
        process_game_data(invalid_game_data)

# Test that the validation logic identifies missing price
def test_missing_price_validation():
    game = valid_game_data[0].copy()
    game["price"] = None  # Set price to None, which should trigger a validation failure
    result = validate_game_data(game)
    assert result == False, f"Validation failed for missing price: {game}"

# Test that the validation logic identifies missing game title
def test_missing_title_validation():
    game = valid_game_data[1].copy()
    game["title"] = None  # Set title to None, which should trigger a validation failure
    result = validate_game_data(game)
    assert result == False, f"Validation failed for missing title: {game}"

# Test that invalid price is caught (negative price)
def test_invalid_price():
    game = valid_game_data[1].copy()
    game["price"] = -1  # Set a negative price, which is invalid
    result = validate_game_data(game)
    assert result == False, f"Validation failed for invalid price: {game}"

