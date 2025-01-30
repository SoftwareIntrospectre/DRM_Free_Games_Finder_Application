from pyspark.sql import DataFrame

def process_steam_data(steam_df: DataFrame) -> DataFrame:
    """Process the Steam data before inserting into the steam_games table."""
    # Example processing steps for Steam data (you can add more)
    return steam_df.select(
        "steam_game_id", "steam_game_name", "price", "developer", "publisher",
        "release_date", "on_windows_pc_platform", "on_mac_platform_bool", "on_linux_platform_bool"
    )

def process_gog_data(gog_df: DataFrame) -> DataFrame:
    """Process the GOG data before inserting into the gog_games table."""
    # Example processing steps for GOG data (you can add more)
    return gog_df.select(
        "gog_game_id", "gog_game_name", "price", "developer", "publisher",
        "release_date", "on_windows_pc_platform", "on_mac_platform_bool", "on_linux_platform_bool"
    )
