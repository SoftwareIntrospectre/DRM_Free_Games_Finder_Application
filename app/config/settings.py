import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # FastAPI Settings
    app_name: str = "DRM-Free Game Comparison Tool"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Database Settings (Snowflake)
    snowflake_account: str = os.getenv("SNOWFLAKE_ACCOUNT", "your_account_name")
    snowflake_user: str = os.getenv("SNOWFLAKE_USER", "your_username")
    snowflake_password: str = os.getenv("SNOWFLAKE_PASSWORD", "your_password")
    snowflake_database: str = os.getenv("SNOWFLAKE_DATABASE", "your_database")
    snowflake_schema: str = os.getenv("SNOWFLAKE_SCHEMA", "your_schema")
    
    # API keys for Steam and GOG
    steam_api_key: str = os.getenv("STEAM_API_KEY", "your_steam_api_key")
    gog_api_key: str = os.getenv("GOG_API_KEY", "your_gog_api_key")
    
    # AWS Settings (for ECS, CloudWatch, etc.)
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "your_aws_access_key")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "your_aws_secret_key")
    aws_region: str = os.getenv("AWS_REGION", "us-west-2")

    # Other settings
    log_level: str = "INFO"

    class Config:
        env_file = ".env"  # Optional: specify a .env file to load environment variables

settings = Settings()
