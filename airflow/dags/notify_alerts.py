import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.dates import timedelta

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def send_failure_email(context):
    """
    Sends an email notification on task failure using environment variables for sensitive info.
    """
    subject = f"Airflow Task Failed: {context['task_instance'].task_id}"
    body = f"Task {context['task_instance'].task_id} failed due to: {context['exception']}\n\nDetails:\n{context['task_instance'].xcom_pull()}"
    
    # Fetch environment variables for email credentials
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')  # Ensure this variable is set securely in your environment

    # Check if the environment variables are set
    if not from_email or not to_email or not password:
        raise ValueError("Missing required environment variables for email configuration.")

    # Email server settings (example using Gmail)
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')  # Default to Gmail if not specified
    smtp_port = int(os.getenv('SMTP_PORT', 587))  # Default to 587 if not specified

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(from_email, password)  # Log in with the credentials
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)  # Send the email
        print(f"Alert email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")

# Instantiate the DAG
dag = DAG(
    'notify_alerts',
    default_args=default_args,
    description='Notify stakeholders about task failures',
    schedule_interval=None,  # This DAG doesn't need to run on a schedule
    start_date=days_ago(1),
    catchup=False,
)

# Task to send failure email
notify_failure_task = PythonOperator(
    task_id='notify_failure_email',
    python_callable=send_failure_email,
    provide_context=True,
    trigger_rule='one_failed',
    dag=dag
)
