import requests
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when
from pyspark.sql import DataFrame

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://api.gog.com"  # Base GOG API URL

# Initialize Spark session
spark = SparkSession.builder \
    .appName("GOG API Data Ingestion") \
    .getOrCreate()

def format_date(date_string):
    """Format date from string (handle nulls/empty values)."""
    return to_date(col(date_string), "yyyy-MM-dd") if date_string else None

def clean_price(price):
    """Clean and format price field."""
    return float(price) if price else None

def clean_discount(discount):
    """Clean and return the discount percentage."""
    return float(discount) if discount else 0.0

def safe_get_price(product, price_type):
    """Safely retrieve the price."""
    return product.get(f'{price_type}Money', {}).get('amount', None)

def safe_get_discount(product):
    """Safely retrieve discount."""
    return product.get('price', {}).get('discount', 0)

def safe_get_discount_amount(product):
    """Safely retrieve discount amount."""
    return product.get('price', {}).get('discountAmount', 0)

def fetch_total_products() -> int:
    """Fetch total number of products in the GOG store."""
    response = requests.get(f"{BASE_URL}/catalog", params={"limit": 1})
    if response.status_code != 200:
        logging.error("Failed to fetch total products count.")
        return 0  # Return 0 if the request fails
    data = response.json()
    return data.get("productCount", 0)

def fetch_gog_data(page: int, batch_size: int = 48) -> DataFrame:
    """Fetch paginated data from GOG API and process into DataFrame."""
    response = requests.get(f"{BASE_URL}/catalog", params={
        "limit": batch_size,
        "page": page,
        "order": "asc:alphabetical",
        "productType": "in:game"  # You can adjust this to filter for specific product types like DLCs, etc.
    })
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch GOG data for page {page}.")
        return spark.createDataFrame([])  # Return empty DataFrame on failure
    
    gog_data = response.json()

    # Extract the list of games from the API response
    game_list = gog_data.get("products", [])

    # Convert the list of GOG games into a PySpark DataFrame
    df = spark.read.json(spark.sparkContext.parallelize(game_list))

    # Clean and process the data (dates, platforms, etc.)
    df = df.withColumn(
        "release_date", format_date("releaseDate")
    ).withColumn(
        "store_release_date", format_date("storeReleaseDate")
    ).withColumn(
        "FinalPrice", clean_price(safe_get_price(col("price"), 'final'))
    ).withColumn(
        "OriginalPrice", clean_price(safe_get_price(col("price"), 'base'))
    ).withColumn(
        "PriceDiscountPercentage", clean_discount(safe_get_discount(col("price")))
    ).withColumn(
        "PriceDiscountAmount", safe_get_discount_amount(col("price"))
    ).withColumn(
        "PriceCurrency", col("price.currency")
    ).withColumn(
        "productState", col("productState")
    ).withColumn(
        "storeLink", col("storeLink")
    ).withColumn(
        "Developer", col("developers").getItem(0)  # Safe get the first developer
    ).withColumn(
        "Publisher", col("publishers").getItem(0)  # Safe get the first publisher
    ).withColumn(
        "OperatingSystem1", col("operatingSystems").getItem(0)  # Get the first operating system
    ).withColumn(
        "OperatingSystem2", col("operatingSystems").getItem(1)  # Get the second operating system
    ).withColumn(
        "OperatingSystem3", col("operatingSystems").getItem(2)  # Get the third operating system
    ).withColumn(
        "Tag1", col("tags").getItem(0)  # Get the first tag
    ).withColumn(
        "Tag2", col("tags").getItem(1)  # Get the second tag
    ).withColumn(
        "Tag3", col("tags").getItem(2)  # Get the third tag
    ).withColumn(
        "Tag4", col("tags").getItem(3)  # Get the fourth tag
    ).withColumn(
        "Tag5", col("tags").getItem(4)  # Get the fifth tag
    ).withColumn(
        "Tag6", col("tags").getItem(5)  # Get the sixth tag
    ).withColumn(
        "Tag7", col("tags").getItem(6)  # Get the seventh tag
    ).withColumn(
        "Tag8", col("tags").getItem(7)  # Get the eighth tag
    ).withColumn(
        "Tag9", col("tags").getItem(8)  # Get the ninth tag
    ).withColumn(
        "Tag10", col("tags").getItem(9)  # Get the tenth tag
    )

    # Filter out invalid games (e.g., free games, missing price)
    df = df.filter(
        (col("FinalPrice") > 0) &
        (col("productState") == "active")
    ).dropDuplicates(["id"])

    return df

def fetch_all_gog_data() -> DataFrame:
    """Fetch all GOG data (across pages) and process into a single DataFrame."""
    
    # First, fetch the total number of products available on GOG
    total_products = fetch_total_products()

    # If no products are found, log an error and return an empty DataFrame
    if total_products == 0:
        logging.error("No products found.")
        return spark.createDataFrame([])

    # Initialize an empty list to collect the data from each page
    all_data = []

    # Define the batch size (number of products to fetch per page)
    batch_size = 48

    # Calculate the total number of pages needed based on total products and batch size
    total_pages = (total_products // batch_size) + 1  # Add 1 to account for any remainder

    # Loop through each page, fetching and processing the data for that page
    for page in range(1, total_pages + 1):
        logging.info(f"Fetching data for page {page}/{total_pages}...")  # Log progress
        # Fetch data for the current page
        page_data = fetch_gog_data(page, batch_size)
        
        # If the fetched data contains valid records, add it to the list of all data
        if page_data.count() > 0:
            all_data.append(page_data)

    # Combine (union) all the data from each page into a single DataFrame
    # Start with the first page of data, or create an empty DataFrame if no data was fetched
    final_df = all_data[0] if all_data else spark.createDataFrame([])

    # Append data from the remaining pages to the final DataFrame
    for df in all_data[1:]:
        final_df = final_df.union(df)

    # Return the final DataFrame containing all the GOG game data across pages
    return final_df