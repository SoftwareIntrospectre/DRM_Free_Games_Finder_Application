from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.email.operators.email import EmailOperator
from datetime import datetime, timedelta

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['your-email@example.com'],  # Email to notify in case of failure
}

# Function to send a custom alert
def send_alert():
    print("Sending an alert! An error occurred in the pipeline.")

# Define the DAG
with DAG(
    'notify_alerts',
    default_args=default_args,
    description='Send notifications if a task fails',
    schedule_interval=None,  # Manually triggered for failures
    start_date=datetime(2025, 1, 29),
    catchup=False,
) as dag:

    # Task 1: Run alert function if a task fails
    alert_task = PythonOperator(
        task_id='send_alert',
        python_callable=send_alert,
    )

    # Task 2: Send email notification in case of failure
    failure_notification = EmailOperator(
        task_id='send_failure_email',
        to='your-email@example.com',
        subject='Airflow Task Failed',
        html_content="""<h3>Dear User,</h3>
                        <p>The task in your Airflow pipeline has failed. Please check the logs for more details.</p>""",
    )

    # Task dependency: If alert task fails, send email notification
    alert_task >> failure_notification
