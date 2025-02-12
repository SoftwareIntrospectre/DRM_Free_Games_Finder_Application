from pyspark.sql import DataFrame

# Process Steam data
def process_steam_data(steam_df: DataFrame) -> DataFrame:
    """Process the Steam data before inserting into the steam_games table."""
    return steam_df.select(
        # Steam-specific fields
        "steam_game_id",            # Game ID
        "steam_game_name",          # Game Name
        "price",                    # Game Price
        "developer",                # Developer
        "publisher",                # Publisher
        "genre1_id",                # Genre ID
        "genre1_name",              # Genre Name
        "release_date",             # Release Date
        "required_age",             # Required Age
        "on_windows_pc_platform",   # Windows Platform Availability
        "on_apple_mac_platform",    # Mac Platform Availability
        "on_linux_platform"         # Linux Platform Availability
    )

# Process GOG data
def process_gog_data(gog_df: DataFrame) -> DataFrame:
    """Process the GOG data before inserting into the gog_games table."""
    return gog_df.select(
        # GOG-specific fields
        "id",                       # Game ID
        "title",                    # Game Title
        "releaseDate",              # Release Date
        "storeReleaseDate",         # Store Release Date
        "FinalPrice",               # Final Price
        "OriginalPrice",            # Original Price
        "PriceDiscountPercentage",  # Price Discount Percentage
        "PriceDiscountAmount",      # Price Discount Amount
        "PriceCurrency",            # Price Currency
        "productState",             # Product State
        "storeLink",                # Store Link
        "Developer",                # Developer
        "Publisher",                # Publisher
        "OperatingSystem1",         # Primary OS (Windows, Mac, or Linux)
        "OperatingSystem2",         # Secondary OS (Mac, Linux, etc.)
        "OperatingSystem3",         # Tertiary OS
        "Tag1",                     # Tag 1
        "Tag2",                     # Tag 2
        "Tag3",                     # Tag 3
        "Tag4",                     # Tag 4
        "Tag5",                     # Tag 5
        "Tag6",                     # Tag 6
        "Tag7",                     # Tag 7
        "Tag8",                     # Tag 8
        "Tag9",                     # Tag 9
        "Tag10"                     # Tag 10
    )
