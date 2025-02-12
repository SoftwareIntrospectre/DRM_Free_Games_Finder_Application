import requests
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when, lit
from pyspark.sql import DataFrame
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Steam API Data Ingestion") \
    .getOrCreate()

# Steam API URL for fetching app details
STEAM_API_URL = "https://store.steampowered.com/api/appdetails"

def fetch_steam_data(app_ids: list) -> DataFrame:
    """Fetch detailed game data from Steam API and process into DataFrame."""
    
    steam_games_data = []  # List to store processed game details

    for app_id in app_ids:
        # Request data for each Steam app by app ID
        params = {'appids': app_id}
        response = requests.get(STEAM_API_URL, params=params)
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch data for app ID {app_id}.")
            continue
        
        steam_data = response.json()
        
        # Check if data exists for this app ID in the response
        if not steam_data.get(str(app_id), {}).get("success", False):
            logging.warning(f"No valid data for app ID {app_id}. Skipping.")
            continue
        
        game_details = steam_data[str(app_id)].get('data', {})

        # Extract relevant game data
        steam_game_id = game_details.get('steam_appid', None)
        steam_game_name = game_details.get('name', '')
        release_date_raw = game_details.get('release_date', {}).get('date', 'N/A')
        price_str = game_details.get('price_overview', {}).get('final_formatted', '').replace('$', '')
        price = float(price_str) if price_str else 0
        is_free = game_details.get('is_free', False)
        
        developer = game_details.get('developers', ['N/A'])[0]
        publisher = game_details.get('publishers', ['N/A'])[0]
        
        # Extract platform availability
        on_windows_pc_platform = str(game_details.get('platforms', {}).get('windows', False))
        on_mac_platform_bool = str(game_details.get('platforms', {}).get('mac', False))
        on_linux_platform_bool = str(game_details.get('platforms', {}).get('linux', False))
        
        # Extract genres (first genre only for simplicity)
        genre1_id = game_details['genres'][0]['id'] if game_details.get('genres') else 'N/A'
        genre1_name = game_details['genres'][0]['description'] if game_details.get('genres') else 'N/A'

        # Validate game data
        if price <= 0 or is_free:
            logging.info(f"App ID {app_id} is either free or has no valid price. Skipping.")
            continue  # Skip invalid games

        # Process and add to list
        steam_games_data.append({
            "steam_game_id": steam_game_id,
            "steam_game_name": steam_game_name,
            "release_date": release_date_raw,
            "price": price,
            "developer": developer,
            "publisher": publisher,
            "genre1_id": genre1_id,
            "genre1_name": genre1_name,
            "on_windows_pc_platform": on_windows_pc_platform,
            "on_mac_platform_bool": on_mac_platform_bool,
            "on_linux_platform_bool": on_linux_platform_bool
        })
    
    # Convert the list of dictionaries into a PySpark DataFrame
    df = spark.createDataFrame(steam_games_data)

    # Clean and process the data (e.g., parsing release date)
    df = df.withColumn(
        "release_date", to_date(col("release_date"), "MMM dd, yyyy")
    ).withColumn(
        "on_windows_pc_platform", when(col("on_windows_pc_platform") == 'True', 1).otherwise(0)
    ).withColumn(
        "on_mac_platform_bool", when(col("on_mac_platform_bool") == 'True', 1).otherwise(0)
    ).withColumn(
        "on_linux_platform_bool", when(col("on_linux_platform_bool") == 'True', 1).otherwise(0)
    )

    # Filter out games with invalid or future release dates (similar to Script A)
    df = df.filter(
        (col("release_date").isNotNull()) & 
        (col("release_date") <= datetime.now())
    ).dropDuplicates(["steam_game_id"])

    logging.info(f"Successfully fetched and processed data for {len(df)} Steam games.")
    
    return df
