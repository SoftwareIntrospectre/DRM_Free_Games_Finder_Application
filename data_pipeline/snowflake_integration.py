import snowflake.connector
from pyspark.sql import DataFrame
from snowflake.connector.pandas_tools import pd_writer

# Import Snowflake config
from snowflake_config import SNOWFLAKE_CONN_PARAMS

def insert_to_snowflake(df: DataFrame, table_name: str):
    """Insert data from DataFrame into Snowflake table."""
    
    # Convert DataFrame to Pandas DataFrame for Snowflake
    pandas_df = df.toPandas()

    # Establish a Snowflake connection
    conn = snowflake.connector.connect(**SNOWFLAKE_CONN_PARAMS)
    cursor = conn.cursor()

    try:
        # Use PandasWriter to upload the DataFrame to Snowflake
        pandas_df.to_sql(table_name, con=conn, index=False, if_exists='replace', method=pd_writer)
        print(f"Data successfully inserted into {table_name}")
    except Exception as e:
        print(f"Error inserting data into Snowflake: {e}")
    finally:
        cursor.close()
        conn.close()
