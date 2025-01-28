from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd

def fetch_steam_data():
    # Fetch data from Steam API
    steam_api_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2"
    response = requests.get(steam_api_url)
    steam_data = response.json()
    return steam_data

def process_data(steam_data):
    # Process the Steam data (example using pandas)
    df = pd.DataFrame(steam_data['applist']['apps'])
    return df

def load_to_snowflake(df):
    # Example function to load data into Snowflake (this could be replaced with actual logic)
    print("Data loaded to Snowflake successfully!")
    return True

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 29),
}

dag = DAG('ETL_dag', default_args=default_args, schedule_interval='@daily')

task_fetch_steam = PythonOperator(
    task_id='fetch_steam_data',
    python_callable=fetch_steam_data,
    dag=dag,
)

task_process_data = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    op_args=['{{ task_instance.xcom_pull(task_ids="fetch_steam_data") }}'],
    dag=dag,
)

task_load_to_snowflake = PythonOperator(
    task_id='load_to_snowflake',
    python_callable=load_to_snowflake,
    op_args=['{{ task_instance.xcom_pull(task_ids="process_data") }}'],
    dag=dag,
)

task_fetch_steam >> task_process_data >> task_load_to_snowflake
