import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger("airflow.task")

# List of supported date formats
DATE_FORMATS = [
    '%b %d, %Y',         # Example: Mar 25, 2022
    '%Y-%m-%d',          # Example: 2022-03-25
    '%d/%m/%Y',          # Example: 25/03/2022
    '%m/%d/%Y',          # Example: 03/25/2022
    '%d-%m-%Y',          # Example: 25-03-2022
    '%Y/%m/%d'           # Example: 2022/03/25
]

# Validate Steam data
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
        logger.error(f"Missing or invalid 'steam_game_id' in data: {steam_data}")
        return False
    if 'steam_game_name' not in steam_data or not isinstance(steam_data['steam_game_name'], str) or not steam_data['steam_game_name'].strip():
        logger.error(f"Missing or invalid 'steam_game_name' in data: {steam_data}")
        return False
    if 'price' not in steam_data or not isinstance(steam_data['price'], (float, int)) or steam_data['price'] < 0:
        logger.error(f"Missing or invalid 'price' in data: {steam_data}")
        return False
    if 'release_date' not in steam_data or not validate_date(steam_data['release_date']):
        logger.error(f"Missing or invalid 'release_date' in data: {steam_data}")
        return False
    if 'developer' not in steam_data or not isinstance(steam_data['developer'], str) or not steam_data['developer'].strip():
        logger.error(f"Missing or invalid 'developer' in data: {steam_data}")
        return False
    if 'publisher' not in steam_data or not isinstance(steam_data['publisher'], str) or not steam_data['publisher'].strip():
        logger.error(f"Missing or invalid 'publisher' in data: {steam_data}")
        return False
    if 'genre1_id' not in steam_data or not isinstance(steam_data['genre1_id'], int):
        logger.error(f"Missing or invalid 'genre1_id' in data: {steam_data}")
        return False
    if 'genre1_name' not in steam_data or not isinstance(steam_data['genre1_name'], str) or not steam_data['genre1_name'].strip():
        logger.error(f"Missing or invalid 'genre1_name' in data: {steam_data}")
        return False
    if 'on_windows_pc_platform' not in steam_data or not isinstance(steam_data['on_windows_pc_platform'], bool):
        logger.error(f"Missing or invalid 'on_windows_pc_platform' in data: {steam_data}")
        return False
    if 'on_apple_mac_platform' not in steam_data or not isinstance(steam_data['on_apple_mac_platform'], bool):
        logger.error(f"Missing or invalid 'on_apple_mac_platform' in data: {steam_data}")
        return False
    if 'on_linux_platform' not in steam_data or not isinstance(steam_data['on_linux_platform'], bool):
        logger.error(f"Missing or invalid 'on_linux_platform' in data: {steam_data}")
        return False

    # If all checks pass, return True
    return True

# Validate GOG data
def validate_gog_data(gog_data):
    """
    Validate the GOG game data.
    Args:
        gog_data (dict): The GOG game data to validate.
    Returns:
        bool: True if the data is valid, False otherwise.
    """
    # Validate required fields and their types
    if 'id' not in gog_data or not isinstance(gog_data['id'], int):
        logger.error(f"Missing or invalid 'id' in data: {gog_data}")
        return False
    if 'title' not in gog_data or not isinstance(gog_data['title'], str) or not gog_data['title'].strip():
        logger.error(f"Missing or invalid 'title' in data: {gog_data}")
        return False
    if 'FinalPrice' not in gog_data or not isinstance(gog_data['FinalPrice'], (float, int)) or gog_data['FinalPrice'] < 0:
        logger.error(f"Missing or invalid 'FinalPrice' in data: {gog_data}")
        return False
    if 'releaseDate' not in gog_data or not validate_date(gog_data['releaseDate']):
        logger.error(f"Missing or invalid 'releaseDate' in data: {gog_data}")
        return False
    if 'Developer' not in gog_data or not isinstance(gog_data['Developer'], str) or not gog_data['Developer'].strip():
        logger.error(f"Missing or invalid 'Developer' in data: {gog_data}")
        return False
    if 'Publisher' not in gog_data or not isinstance(gog_data['Publisher'], str) or not gog_data['Publisher'].strip():
        logger.error(f"Missing or invalid 'Publisher' in data: {gog_data}")
        return False
    if 'OperatingSystem1' not in gog_data or not isinstance(gog_data['OperatingSystem1'], str) or not gog_data['OperatingSystem1'].strip():
        logger.error(f"Missing or invalid 'OperatingSystem1' in data: {gog_data}")
        return False

    # Check for valid optional tags (can be empty or missing)
    for tag in ['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7', 'Tag8', 'Tag9', 'Tag10']:
        if tag in gog_data and (gog_data[tag] and not isinstance(gog_data[tag], str)):
            logger.error(f"Invalid {tag} in data: {gog_data}")
            return False

    # If all checks pass, return True
    return True

# Validate Date
def validate_date(date_str):
    """
    Validates if the date is in the correct format and not in the future.
    Args:
        date_str (str): The date string to validate.
    Returns:
        bool: True if the date is valid, False otherwise.
    """
    for date_format in DATE_FORMATS:
        try:
            release_date = datetime.strptime(date_str, date_format)
            # Check if the date is in the future
            if release_date > datetime.now():
                logger.error(f"Release date {date_str} is in the future.")
                return False
            return True
        except ValueError:
            continue  # Try next date format

    logger.error(f"Invalid date format for release date: {date_str}")
    return False

# Validate No Duplicates
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
            logger.error(f"Duplicate game found with ID: {game_id}")
            return False
        seen_ids.add(game_id)
    return True

# Main Validation Function
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
        {"steam_game_id": 1, "steam_game_name": "Game A", "price": 19.99, "release_date": "Mar 25, 2022", "developer": "Dev A", "publisher": "Pub A", "genre1_id": 101, "genre1_name": "Action", "on_windows_pc_platform": True, "on_apple_mac_platform": True, "on_linux_platform": False},
        {"steam_game_id": 2, "steam_game_name": "Game B", "price": 0, "release_date": "Nov 01, 2021", "developer": "Dev B", "publisher": "Pub B", "genre1_id": 102, "genre1_name": "RPG", "on_windows_pc_platform": True, "on_apple_mac_platform": False, "on_linux_platform": True}
    ]
    gog_data = [
        {"id": 101, "title": "Game X", "FinalPrice": 9.99, "releaseDate": "2020-01-15", "Developer": "Dev X", "Publisher": "Pub X", "OperatingSystem1": "Windows", "Tag1": "Strategy"},
        {"id": 102, "title": "Game Y", "FinalPrice": 15.99, "releaseDate": "07/22/2019", "Developer": "Dev Y", "Publisher": "Pub Y", "OperatingSystem1": "Mac", "Tag2": "Adventure"}
    ]

    if validate_data(steam_data, gog_data):
        logger.info("Data validation passed successfully.")
    else:
        logger.error("Data validation failed. Please check the logs for details.")
