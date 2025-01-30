import requests
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when
from pyspark.sql import DataFrame

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GOG_API_URL = "https://api.gog.com/games"  # Example GOG API endpoint

# Initialize Spark session
spark = SparkSession.builder \
    .appName("GOG API Data Ingestion") \
    .getOrCreate()

def fetch_gog_data() -> DataFrame:
    """Fetch data from GOG API and process into DataFrame."""
    response = requests.get(GOG_API_URL)
    if response.status_code != 200:
        logging.error("Failed to fetch GOG data.")
        return spark.createDataFrame([])  # Return empty DataFrame on failure

    gog_data = response.json()

    # Example data extraction (this will change based on actual API response)
    game_list = gog_data.get("games", [])

    # Convert the list of GOG games into a PySpark DataFrame
    df = spark.read.json(spark.sparkContext.parallelize(game_list))

    # Clean and process the data
    df = df.withColumn(
        "release_date", to_date(col("release_date"), "yyyy-MM-dd")
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
    ).dropDuplicates(["gog_game_id"])

    return df
