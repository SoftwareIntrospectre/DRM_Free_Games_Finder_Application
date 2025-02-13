def create_steam_table():
    return """
    CREATE TABLE IF NOT EXISTS steam_games (
        game_id STRING PRIMARY KEY,
        game_title STRING NOT NULL,
        steam_link STRING,
        game_release_date DATE,
        final_price FLOAT,
        original_price FLOAT,
        price_discount_percentage FLOAT,
        price_discount_amount FLOAT,
        price_currency STRING,
        product_state STRING,
        developer STRING,
        publisher STRING,
        operating_systems ARRAY,
        tags ARRAY,
        stage_record_loaded_datetime TIMESTAMP_NTZ,
        stage_record_filename STRING,
        game_release_date DATE,
        developer STRING,
        publisher STRING
    );
    """

def create_gog_table():
    return """
    CREATE TABLE IF NOT EXISTS gog_games (
        game_id STRING PRIMARY KEY,
        game_title STRING NOT NULL,
        gog_link STRING,
        game_release_date DATE,
        final_price FLOAT,
        original_price FLOAT,
        price_discount_percentage FLOAT,
        price_discount_amount FLOAT,
        price_currency STRING,
        product_state STRING,
        developer STRING,
        publisher STRING,
        operating_systems ARRAY,
        tags ARRAY,
        stage_record_loaded_datetime TIMESTAMP_NTZ,
        stage_record_filename STRING,
        game_release_date DATE,
        developer STRING,
        publisher STRING
    );
    """
