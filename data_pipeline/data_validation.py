import logging
from pyspark.sql import DataFrame

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_data(df: DataFrame):
    """
    Performs validation on the processed game data.

    Args:
    - df: DataFrame to validate.

    Returns:
    - is_valid: Boolean indicating whether the data is valid.
    - issues: List of issues (if any).
    """
    issues = []

    # Check for missing important fields like game_id, title, price, and platform
    if df.filter("game_id IS NULL OR title IS NULL OR price IS NULL OR platform IS NULL").count() > 0:
        issues.append("Missing required fields (game_id, title, price, platform).")
    
    # Check for duplicate game IDs (assuming game_id should be unique)
    if df.groupBy("game_id").count().filter("count > 1").count() > 0:
        issues.append("Duplicate game IDs found.")
    
    # Check if any game has no platform info
    if df.filter("platform IS NULL").count() > 0:
        issues.append("Games with missing platform information found.")
    
    # Check if the game status is valid (this can depend on your use case)
    if df.filter("game_status IS NULL").count() > 0:
        issues.append("Games with missing game status found.")

    is_valid = len(issues) == 0

    # Log the issues
    if not is_valid:
        logger.error(f"Data validation failed: {issues}")
    else:
        logger.info("Data validation passed successfully.")

    return is_valid, issues

def main():
    # Example: Load processed data (this can be replaced with the actual processed data location)
    processed_data = spark.read.parquet("processed_game_data.parquet")

    # Validate the data
    is_valid, issues = validate_data(processed_data)

    if is_valid:
        logger.info("Data is valid and ready for further processing.")
    else:
        logger.warning(f"Data validation issues found: {issues}")

if __name__ == "__main__":
    main()
