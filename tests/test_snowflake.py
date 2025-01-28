import pytest
from snowflake.snowflake_config import connect_to_snowflake

def test_snowflake_connection():
    conn = connect_to_snowflake()
    assert conn is not None
