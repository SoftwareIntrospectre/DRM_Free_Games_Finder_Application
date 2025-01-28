from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Game Data Processing") \
    .getOrCreate()

def process_steam_gog_data(steam_data_df, gog_data_df):
    """
    Processes the Steam and GOG data to merge, clean, and prepare it for storage.

    Args:
    - steam_data_df: DataFrame containing Steam data.
    - gog_data_df: DataFrame containing GOG data.

    Returns:
    - processed_df: Cleaned and merged DataFrame with Steam and GOG game info.
    """
    
    # Clean and transform Steam data
    steam_data_cleaned = steam_data_df \
        .dropna(subset=["game_id", "title", "price"]) \
        .withColumn("platform", when(col("platform") == "Steam", "Steam").otherwise("Unknown"))
    
    # Clean and transform GOG data
    gog_data_cleaned = gog_data_df \
        .dropna(subset=["game_id", "title", "price"]) \
        .withColumn("platform", when(col("platform") == "GOG", "GOG").otherwise("Unknown")) \
        .withColumn("is_drm_free", when(col("is_drm_free") == True, "Yes").otherwise("No"))
    
    # Merge Steam and GOG data on 'game_id'
    merged_data = steam_data_cleaned.join(gog_data_cleaned, on="game_id", how="outer")
    
    # Example of a data transformation (add additional processing as needed)
    merged_data = merged_data \
        .withColumn("game_status", 
                    when(col("platform") == "Steam", "Exclusive on Steam")
                    .when(col("platform") == "GOG", "Exclusive on GOG")
                    .otherwise("Available on both platforms"))

    return merged_data

def main():
    # Example: Load Steam and GOG data as DataFrames
    steam_data = spark.read.json("path_to_steam_data.json")
    gog_data = spark.read.json("path_to_gog_data.json")
    
    # Process the data
    processed_data = process_steam_gog_data(steam_data, gog_data)
    
    # Show processed data
    processed_data.show()

    # Optionally, save to Snowflake or file
    # processed_data.write.format("snowflake").options(**snowflake_options).save()
    # Or save to local storage (for example, Parquet file)
    processed_data.write.parquet("processed_game_data.parquet")

if __name__ == "__main__":
    main()
