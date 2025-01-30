# pip install snowflake-connector-python
# pip install snowflake-sqlalchemy

# snowflake_config.py
import os

# Snowflake credentials (ensure you set them as environment variables or hardcode them for local dev)
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT', 'replace_with_my_account')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER', 'replace_with_my_user')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD', 'replace_with_my_password')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE', 'replace_with_my_warehouse')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE', 'replace_with_my_database')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA', 'replace_with_my_schema')

# Connection details for Snowflake
SNOWFLAKE_CONN_PARAMS = {
    'user': SNOWFLAKE_USER,
    'password': SNOWFLAKE_PASSWORD,
    'account': SNOWFLAKE_ACCOUNT,
    'warehouse': SNOWFLAKE_WAREHOUSE,
    'database': SNOWFLAKE_DATABASE,
    'schema': SNOWFLAKE_SCHEMA
}
