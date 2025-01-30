import requests
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when
from pyspark.sql import DataFrame

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STEAM_API_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2"  # Example Steam API endpoint

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Steam API Data Ingestion") \
    .getOrCreate()

def fetch_steam_data() -> DataFrame:
    """Fetch data from Steam API and process into DataFrame."""
    response = requests.get(STEAM_API_URL)
    if response.status_code != 200:
        logging.error("Failed to fetch Steam data.")
        return spark.createDataFrame([])  # Return empty DataFrame on failure

    steam_data = response.json()

    # Example data extraction (this will change based on actual API response)
    app_list = steam_data.get("applist", {}).get("apps", [])

    # Convert the list of Steam apps into a PySpark DataFrame
    df = spark.read.json(spark.sparkContext.parallelize(app_list))

    # Clean and process the data
    df = df.withColumn(
        "release_date", to_date(col("release_date"), "MMM dd, yyyy")
    ).withColumn(
        "on_windows_pc_platform", when(col("on_windows_pc_platform") == 'True', 1).otherwise(0)
    ).withColumn(
        "on_mac_platform_bool", when(col("on_mac_platform_bool") == 'True', 1).otherwise(0)
    ).withColumn(
        "on_linux_platform_bool", when(col("on_linux_platform_bool") == 'True', 1).otherwise(0)
    )

    # Filter out invalid games (e.g., free games, missing data)
    df = df.filter(
        (col("game_type") == "game") &
        (col("is_free") == 'False') &
        (col("price") > 0)
    ).dropDuplicates(["steam_game_id"])

    return df
