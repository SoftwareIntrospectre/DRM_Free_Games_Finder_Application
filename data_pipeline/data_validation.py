import logging
import re
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='./data/logs/data_validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_steam_data(steam_data):
    """
    Validate the Steam game data.
    Args:
        steam_data (dict): The Steam game data to validate.
    Returns:
        bool: True if the data is valid, False otherwise.
    """
    # Validate required fields and their types
    if 'steam_game_id' not in steam_data or not isinstance(steam_data['steam_game_id'], int):
        logging.error(f"Missing or invalid 'steam_game_id' in data: {steam_data}")
        return False
    if 'name' not in steam_data or not isinstance(steam_data['name'], str) or not steam_data['name'].strip():
        logging.error(f"Missing or invalid 'name' in data: {steam_data}")
        return False
    if 'price' not in steam_data or not isinstance(steam_data['price'], (float, int)) or steam_data['price'] < 0:
        logging.error(f"Missing or invalid 'price' in data: {steam_data}")
        return False
    if 'release_date' not in steam_data or not validate_date(steam_data['release_date']):
        logging.error(f"Missing or invalid 'release_date' in data: {steam_data}")
        return False
    
    # Validate specific price range or logic if necessary
    if steam_data['price'] == 0:
        logging.warning(f"Game {steam_data['steam_game_id']} has a price of 0, which might be incorrect: {steam_data}")

    # If all checks pass, return True
    return True

def validate_gog_data(gog_data):
    """
    Validate the GOG game data.
    Args:
        gog_data (dict): The GOG game data to validate.
    Returns:
        bool: True if the data is valid, False otherwise.
    """
    # Validate required fields and their types
    if 'gog_game_id' not in gog_data or not isinstance(gog_data['gog_game_id'], int):
        logging.error(f"Missing or invalid 'gog_game_id' in data: {gog_data}")
        return False
    if 'name' not in gog_data or not isinstance(gog_data['name'], str) or not gog_data['name'].strip():
        logging.error(f"Missing or invalid 'name' in data: {gog_data}")
        return False
    if 'price' not in gog_data or not isinstance(gog_data['price'], (float, int)) or gog_data['price'] < 0:
        logging.error(f"Missing or invalid 'price' in data: {gog_data}")
        return False
    if 'release_date' not in gog_data or not validate_date(gog_data['release_date']):
        logging.error(f"Missing or invalid 'release_date' in data: {gog_data}")
        return False
    
    # Validate specific price range or logic if necessary
    if gog_data['price'] == 0:
        logging.warning(f"Game {gog_data['gog_game_id']} has a price of 0, which might be incorrect: {gog_data}")

    # If all checks pass, return True
    return True

def validate_date(date_str):
    """
    Validates if the date is in the correct format and not in the future.
    Args:
        date_str (str): The date string to validate.
    Returns:
        bool: True if the date is valid, False otherwise.
    """
    try:
        # Convert to a datetime object
        release_date = datetime.strptime(date_str, '%b %d, %Y')
        # Check if the date is in the future
        if release_date > datetime.now():
            logging.error(f"Release date {date_str} is in the future.")
            return False
        return True
    except ValueError:
        logging.error(f"Invalid date format for release date: {date_str}")
        return False

def validate_no_duplicates(steam_data, gog_data, seen_ids):
    """
    Check for duplicate game IDs across both Steam and GOG data.
    Args:
        steam_data (list): List of Steam game data.
        gog_data (list): List of GOG game data.
        seen_ids (set): A set to store game IDs that have already been processed.
    Returns:
        bool: True if there are no duplicates, False if duplicates are found.
    """
    for game in steam_data + gog_data:
        game_id = game.get('steam_game_id', game.get('gog_game_id'))
        if game_id in seen_ids:
            logging.error(f"Duplicate game found with ID: {game_id}")
            return False
        seen_ids.add(game_id)
    return True

def validate_data(steam_data, gog_data):
    """
    Validate both Steam and GOG data before processing.
    Args:
        steam_data (list): List of Steam game data to validate.
        gog_data (list): List of GOG game data to validate.
    Returns:
        bool: True if all data is valid, False otherwise.
    """
    valid_steam = all(validate_steam_data(game) for game in steam_data)
    valid_gog = all(validate_gog_data(game) for game in gog_data)

    seen_ids = set()
    no_duplicates = validate_no_duplicates(steam_data, gog_data, seen_ids)

    return valid_steam and valid_gog and no_duplicates

if __name__ == "__main__":
    # Sample data for testing
    steam_data = [
        {"steam_game_id": 1, "name": "Game A", "price": 19.99, "release_date": "Mar 25, 2022"},
        {"steam_game_id": 2, "name": "Game B", "price": 0, "release_date": "Nov 01, 2021"},
    ]
    gog_data = [
        {"gog_game_id": 101, "name": "Game X", "price": 9.99, "release_date": "Jan 15, 2020"},
        {"gog_game_id": 102, "name": "Game Y", "price": 15.99, "release_date": "Jul 22, 2019"},
    ]
    
    if validate_data(steam_data, gog_data):
        logging.info("Data validation passed successfully.")
    else:
        logging.error("Data validation failed. Please check the logs for details.")
