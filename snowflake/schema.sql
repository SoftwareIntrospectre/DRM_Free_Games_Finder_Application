-- Create the table to store game data
CREATE TABLE IF NOT EXISTS game_data (
    game_id STRING PRIMARY KEY,
    game_title STRING NOT NULL,
    steam_link STRING,
    gog_link STRING,
    game_release_date DATE,
    store_release_date DATE,
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
    stage_record_filename STRING
);

-- Create table for tracking metadata for each ETL load
CREATE TABLE IF NOT EXISTS data_load_metadata (
    load_id STRING PRIMARY KEY,
    load_start_time TIMESTAMP_NTZ,
    load_end_time TIMESTAMP_NTZ,
    load_status STRING,  -- e.g. 'success', 'failure'
    records_loaded INT,
    records_failed INT,
    error_message STRING
);

-- Create table to store errors related to the ETL process
CREATE TABLE IF NOT EXISTS etl_errors (
    error_id STRING PRIMARY KEY,
    error_message STRING,
    error_timestamp TIMESTAMP_NTZ,
    error_level STRING,  -- e.g., 'warning', 'error'
    affected_record_id STRING
);

-- Example of a table to store statistics for reporting purposes
CREATE TABLE IF NOT EXISTS game_statistics (
    stat_id STRING PRIMARY KEY,
    total_steam_games INT,
    total_gog_games INT,
    games_with_drm_free_gog_version INT,
    load_datetime TIMESTAMP_NTZ
);

-- Create a staging table to temporarily store incoming raw data from APIs
CREATE TABLE IF NOT EXISTS gog_games_staging (
    stage_record_id STRING PRIMARY KEY,
    game_id STRING,
    game_title STRING,
    game_release_date DATE,
    store_release_date DATE,
    final_price FLOAT,
    original_price FLOAT,
    price_discount_percentage FLOAT,
    price_discount_amount FLOAT,
    price_currency STRING,
    product_state STRING,
    store_link STRING,
    developer STRING,
    publisher STRING,
    operating_systems ARRAY,
    tags ARRAY,
    stage_record_loaded_datetime TIMESTAMP_NTZ,
    stage_record_filename STRING
);

-- Create a staging table for Steam game data (if you plan to store Steam data temporarily)
CREATE TABLE IF NOT EXISTS steam_games_staging (
    stage_record_id STRING PRIMARY KEY,
    game_id STRING,
    game_title STRING,
    game_release_date DATE,
    store_release_date DATE,
    final_price FLOAT,
    original_price FLOAT,
    price_discount_percentage FLOAT,
    price_discount_amount FLOAT,
    price_currency STRING,
    product_state STRING,
    store_link STRING,
    developer STRING,
    publisher STRING,
    operating_systems ARRAY,
    tags ARRAY,
    stage_record_loaded_datetime TIMESTAMP_NTZ,
    stage_record_filename STRING
);

-- Optional: Create a table to store logs of user searches or interactions with the application
CREATE TABLE IF NOT EXISTS user_search_logs (
    search_id STRING PRIMARY KEY,
    user_id STRING,
    search_query STRING,
    search_datetime TIMESTAMP_NTZ,
    search_results_count INT
);
