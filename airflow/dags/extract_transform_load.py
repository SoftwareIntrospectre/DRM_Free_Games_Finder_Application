from airflow import DAG
from airflow.providers.http.operators.http import HttpSensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.utils.dates import days_ago
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import timedelta
import logging

from data_pipeline.steam_api import fetch_steam_data
from data_pipeline.gog_api import fetch_gog_data
from data_pipeline.spark_processing import transform_data_to_snowflake
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
    schedule_interval='@daily',  # This could be changed based on your frequency needs
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
extract_steam_data = PythonOperator(
    task_id='extract_steam_data',
    python_callable=fetch_steam_data,
    provide_context=True,
    dag=dag
)

# Task 4: Extract GOG data
extract_gog_data = PythonOperator(
    task_id='extract_gog_data',
    python_callable=fetch_gog_data,
    provide_context=True,
    dag=dag
)

# Task 5: Validate Steam data
validate_steam = PythonOperator(
    task_id='validate_steam_data',
    python_callable=validate_steam_data,
    provide_context=True,
    dag=dag
)

# Task 6: Validate GOG data
validate_gog = PythonOperator(
    task_id='validate_gog_data',
    python_callable=validate_gog_data,
    provide_context=True,
    dag=dag
)

# Task 7: Transform data using Spark (for both Steam and GOG)
transform_data = SparkSubmitOperator(
    task_id='transform_data_to_snowflake',
    application='data_pipeline/spark_processing.py',
    conn_id='spark_default',  # Configure Spark connection in Airflow
    executor_memory='4g',
    total_executor_cores=4,
    dag=dag
)

# Task 8: Load Steam data to Snowflake
load_steam_data = SnowflakeOperator(
    task_id='load_steam_data',
    sql="sql_queries/load_steam_data.sql",  # Adjust SQL based on your Snowflake table schema
    snowflake_conn_id='snowflake_connection',
    autocommit=True,
    dag=dag
)

# Task 9: Load GOG data to Snowflake
load_gog_data = SnowflakeOperator(
    task_id='load_gog_data',
    sql="sql_queries/load_gog_data.sql",  # Adjust SQL based on your Snowflake table schema
    snowflake_conn_id='snowflake_connection',
    autocommit=True,
    dag=dag
)

# Task 10: Notify if the ETL job fails
def notify_failure(context):
    """
    Sends a notification if a task fails.
    """
    subject = f"Task Failed: {context['task_instance'].task_id}"
    message = f"Task {context['task_instance'].task_id} failed. Error: {context['exception']}"
    logging.error(message)
    # Additional notification methods like email can be added here

notify_failure_task = PythonOperator(
    task_id='notify_failure',
    python_callable=notify_failure,
    provide_context=True,
    trigger_rule='one_failed',
    dag=dag
)

# Set task dependencies
check_steam_api >> check_gog_api >> [extract_steam_data, extract_gog_data]
[extract_steam_data, extract_gog_data] >> [validate_steam, validate_gog]
[validate_steam, validate_gog] >> transform_data >> [load_steam_data, load_gog_data]
[load_steam_data, load_gog_data] >> notify_failure_task
