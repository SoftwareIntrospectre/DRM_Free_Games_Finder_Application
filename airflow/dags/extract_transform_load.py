from airflow import DAG
from airflow.providers.http.operators.http import HttpSensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.dates import timedelta
import logging

# Import functions from your data pipeline
from data_pipeline.steam_api import fetch_steam_data
from data_pipeline.gog_api import fetch_gog_data
from data_pipeline.spark_processing import process_steam_data, process_gog_data
from data_pipeline.data_validation import validate_steam_data, validate_gog_data

# Define the default_args dictionary to specify retry configurations, etc.
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'extract_transform_load',
    default_args=default_args,
    description='ETL for Steam and GOG data to Snowflake',
    schedule_interval='@daily',  # Adjust as necessary
    start_date=days_ago(1),
    catchup=False,
)

# Task 1: Check for the availability of the Steam API
check_steam_api = HttpSensor(
    task_id='check_steam_api',
    http_conn_id='steam_api_connection',
    endpoint='/ISteamApps/GetAppList/v2/',
    poke_interval=30,
    timeout=300,
    retries=3,
    poke_interval=60,
    dag=dag
)

# Task 2: Check for the availability of the GOG API
check_gog_api = HttpSensor(
    task_id='check_gog_api',
    http_conn_id='gog_api_connection',
    endpoint='/v1/gog_data',
    poke_interval=30,
    timeout=300,
    retries=3,
    poke_interval=60,
    dag=dag
)

# Task 3: Extract Steam data
# This task fetches data from the Steam API using the fetch_steam_data function
extract_steam_data = PythonOperator(
    task_id='extract_steam_data',
    python_callable=fetch_steam_data,
    provide_context=True,  # Allow the use of context for task execution
    dag=dag
)

# Task 4: Extract GOG data
# This task fetches data from the GOG API using the fetch_gog_data function
extract_gog_data = PythonOperator(
    task_id='extract_gog_data',
    python_callable=fetch_gog_data,
    provide_context=True,  # Allow the use of context for task execution
    dag=dag
)

# Task 5: Validate Steam data
# This task validates the Steam data using the validate_steam_data function
validate_steam = PythonOperator(
    task_id='validate_steam_data',
    python_callable=validate_steam_data,
    provide_context=True,  # Allow the use of context for task execution
    dag=dag
)

# Task 6: Validate GOG data
# This task validates the GOG data using the validate_gog_data function
validate_gog = PythonOperator(
    task_id='validate_gog_data',
    python_callable=validate_gog_data,
    provide_context=True,  # Allow the use of context for task execution
    dag=dag
)

# Task 7: Transform Steam data
# This task processes the raw Steam data into the final format using Spark-based transformation
def transform_steam_data(**kwargs):
    # Fetch Steam data (in your case, replace with actual app IDs)
    steam_df = fetch_steam_data(app_ids=[12345, 67890])  # Example app IDs, adjust as needed
    
    # Process the fetched data with your transformation logic
    processed_steam_df = process_steam_data(steam_df)
    
    # Optionally, log or return processed data here
    return processed_steam_df

transform_steam = PythonOperator(
    task_id='transform_steam_data',
    python_callable=transform_steam_data,
    provide_context=True,  # Allow the use of context for task execution
    dag=dag
)

# Task 8: Transform GOG data
# This task processes the raw GOG data into the final format using Spark-based transformation
def transform_gog_data(**kwargs):
    # Fetch GOG data (you can adjust based on actual fetching logic)
    gog_df = fetch_gog_data()  # Adjust this function based on the real fetching method
    
    # Process the fetched data with your transformation logic
    processed_gog_df = process_gog_data(gog_df)
    
    # Optionally, log or return processed data here
    return processed_gog_df

transform_gog = PythonOperator(
    task_id='transform_gog_data',
    python_callable=transform_gog_data,
    provide_context=True,  # Allow the use of context for task execution
    dag=dag
)

# Task 9: Load Steam data to Snowflake
# This task loads the transformed Steam data into Snowflake
load_steam_data = SnowflakeOperator(
    task_id='load_steam_data',
    sql="sql_queries/load_steam_data.sql",  # Adjust SQL based on your Snowflake schema
    snowflake_conn_id='snowflake_connection',  # Ensure your Snowflake connection is set up correctly in Airflow
    autocommit=True,
    dag=dag
)

# Task 10: Load GOG data to Snowflake
# This task loads the transformed GOG data into Snowflake
load_gog_data = SnowflakeOperator(
    task_id='load_gog_data',
    sql="sql_queries/load_gog_data.sql",  # Adjust SQL based on your Snowflake schema
    snowflake_conn_id='snowflake_connection',  # Ensure your Snowflake connection is set up correctly in Airflow
    autocommit=True,
    dag=dag
)

# Task 11: Notify if the ETL job fails
# This task sends a notification if any task fails during the ETL process
def notify_failure(context):
    """
    Sends a notification if a task fails.
    """
    subject = f"Task Failed: {context['task_instance'].task_id}"
    message = f"Task {context['task_instance'].task_id} failed. Error: {context['exception']}"
    logging.error(message)
    # Additional notification methods (e.g., email) can be added here

notify_failure_task = PythonOperator(
    task_id='notify_failure',
    python_callable=notify_failure,
    provide_context=True,
    trigger_rule='one_failed',  # Trigger this task if any prior task fails
    dag=dag
)

# Set task dependencies
# Task dependencies represent the order of execution of tasks
check_steam_api >> check_gog_api >> [extract_steam_data, extract_gog_data]
[extract_steam_data, extract_gog_data] >> [validate_steam, validate_gog]
[validate_steam, validate_gog] >> [transform_steam, transform_gog]
[transform_steam, transform_gog] >> [load_steam_data, load_gog_data]
[load_steam_data, load_gog_data] >> notify_failure_task