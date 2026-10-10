# Practical 06: Apache Airflow DAG Definition
# Author: Mohammad Ayaan Sajid Shaikh (Roll No: 47, Student ID: 5135870)
import os
from datetime import datetime, timedelta
from airflow import DAG

try:
    from airflow.providers.standard.operators.bash import BashOperator
    from airflow.providers.standard.operators.empty import EmptyOperator
except ImportError:
    from airflow.operators.bash import BashOperator
    from airflow.operators.empty import EmptyOperator

STUDENT_NAME = "Mohammad Ayaan Sajid Shaikh"
EXTRACTION_SCRIPT = os.path.expanduser("~/airflow/dags/data_extraction.py")

default_args = {
    "owner": "data_engineering_lab",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "university_etl_orchestration",
    default_args=default_args,
    description="Lab assignment for API and Flat File ETL orchestration",
    schedule=timedelta(days=1),
    catchup=False,
) as dag:

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    execute_extraction = BashOperator(
        task_id="run_extraction_script",
        bash_command=f"python3 {EXTRACTION_SCRIPT}",
    )

    pipeline_complete = BashOperator(
        task_id="log_pipeline_success",
        bash_command='echo "ETL Execution completed successfully at $(date)"',
    )

    show_student_name = BashOperator(
        task_id="show_student_name",
        bash_command=f'echo "Submitted by: {STUDENT_NAME}"',
    )

    start_pipeline >> execute_extraction >> pipeline_complete >> show_student_name
