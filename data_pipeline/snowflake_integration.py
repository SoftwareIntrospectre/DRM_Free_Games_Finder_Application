import snowflake.connector
from pyspark.sql import DataFrame
from snowflake.connector.pandas_tools import pd_writer

# Import Snowflake config
from snowflake_config import SNOWFLAKE_CONN_PARAMS

def insert_steam_data_to_snowflake(df: DataFrame):
    """Insert Steam data into Snowflake."""
    insert_data_to_snowflake(df, 'steam_games_staging', 'steam_games')

def insert_gog_data_to_snowflake(df: DataFrame):
    """Insert GOG data into Snowflake."""
    insert_data_to_snowflake(df, 'gog_games_staging', 'gog_games')

def insert_data_to_snowflake(df: DataFrame, staging_table: str, final_table: str):
    """Helper function to insert data into Snowflake."""
    
    # Convert DataFrame to Pandas DataFrame for Snowflake
    pandas_df = df.toPandas()

    # Establish a Snowflake connection
    conn = snowflake.connector.connect(**SNOWFLAKE_CONN_PARAMS)
    cursor = conn.cursor()

    try:
        # Insert into the staging table
        pandas_df.to_sql(staging_table, con=conn, index=False, if_exists='append', method=pd_writer)
        print(f"Data successfully inserted into {staging_table}")
        
        # Insert from staging to the final table
        query = f"""
        INSERT INTO {final_table} 
        SELECT * FROM {staging_table}
        ON CONFLICT (game_title, developer, publisher, game_release_date) DO NOTHING;
        """
        cursor.execute(query)
        print(f"Data successfully transferred from staging to {final_table}")

    except Exception as e:
        print(f"Error inserting data into Snowflake: {e}")
    finally:
        cursor.close()
        conn.close()
