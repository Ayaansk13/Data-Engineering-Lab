# Practical-06: Workflow Orchestration and ETL Automation using Apache Airflow

---

## 1. Aim
To design, deploy, and evaluate an automated Directed Acyclic Graph (DAG) using Apache Airflow, configure task execution dependencies across pipeline initialization, Python extraction, and completion logging, and test individual task execution within the Airflow runtime.

---

## 2. Theory

### 2.1 Workflow Orchestration Principles
Modern data engineering pipelines comprise interconnected jobs with complex temporal and logical dependencies. Workflow orchestrators manage these pipelines by:
- **Scheduling:** Triggering jobs based on chronologically defined intervals or external events.
- **Dependency Resolution:** Ensuring downstream tasks execute only upon successful upstream completion.
- **Fault Tolerance & Retries:** Automatically re-executing failed tasks with exponential backoff.
- **Monitoring:** Providing centralized logging and alerting across execution states.

### 2.2 Apache Airflow Architecture
Apache Airflow models workflows as **Directed Acyclic Graphs (DAGs)**:
- **Directed:** Tasks flow in a strict one-way execution path ($A \rightarrow B \rightarrow C$).
- **Acyclic:** No circular loops or infinite recursion allowed.
- **Core Components:**
  - **Scheduler:** Monitors task dependencies and queues runnable tasks.
  - **Executor / Workers:** Executes task instances (Sequential, Local, or Celery Executor).
  - **Metadata Database:** Stores DAG definitions, execution history, and task instance states.
  - **Webserver:** Web UI for DAG inspection, trigger management, and log review.
- **Operators:** Templates for executing specific units of work:
  - `BashOperator`: Executes bash shell commands or scripts.
  - `EmptyOperator` (or `DummyOperator`): No-op milestone anchor defining pipeline boundaries.

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Framework:** Apache Airflow 2.8+ / 3.x (`apache-airflow`)
- **Environment:** Linux / WSL / Google Colab
- **Helper Scripts:** `data_extraction.py`, `data_pipeline_dag.py`

---

## 4. Procedure
1. Install Apache Airflow via `pip install apache-airflow`.
2. Configure the default Airflow DAGs directory (`~/airflow/dags/`).
3. Deploy the data extraction worker script (`data_extraction.py`) into the DAGs folder.
4. Author the DAG definition file (`data_pipeline_dag.py`):
   - Define `default_args` including owner, start date (`2026-01-01`), retry count (`1`), and retry delay (`5 minutes`).
   - Instantiate the DAG context `university_etl_orchestration` with a daily schedule interval (`schedule=timedelta(days=1)`).
   - Configure Task 1 (`start_pipeline`): `EmptyOperator` initializing the workflow.
   - Configure Task 2 (`run_extraction_script`): `BashOperator` executing `python3 ~/airflow/dags/data_extraction.py`.
   - Configure Task 3 (`log_pipeline_success`): `BashOperator` echoing pipeline timestamp completion.
   - Configure Task 4 (`show_student_name`): `BashOperator` echoing student attribution to task logs.
   - Set execution dependencies: `start_pipeline >> execute_extraction >> pipeline_complete >> show_student_name`.
5. Verify DAG syntax and availability using `airflow dags list`.
6. Test each task instance in isolation using `airflow tasks test`.

---

## 5. Code Explanation

### DAG Definition (`data_pipeline_dag.py`)
```python
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
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "university_etl_orchestration",
    default_args=default_args,
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

    # Establish linear task execution dependency
    start_pipeline >> execute_extraction >> pipeline_complete >> show_student_name
```

---

## 6. Sample Input
- **DAG Configuration:**
  - DAG ID: `university_etl_orchestration`
  - Schedule: `@daily` (`timedelta(days=1)`)
  - Execution Date: `2026-01-01`
  - Tasks: 4 sequentially linked tasks

---

## 7. Sample Output
```text
[info] Running: ['airflow', 'tasks', 'test', 'university_etl_orchestration', 'start_pipeline', '2026-01-01']
[info] Task start_pipeline completed successfully.

[info] Running: ['airflow', 'tasks', 'test', 'university_etl_orchestration', 'run_extraction_script', '2026-01-01']
[info] --- Merged ETL Pipeline Data View ---
[info] Data successfully saved to 'cleaned_warehouse_profiles.csv'
[info] Task run_extraction_script completed successfully.

[info] Running: ['airflow', 'tasks', 'test', 'university_etl_orchestration', 'log_pipeline_success', '2026-01-01']
[info] Output: ETL Execution completed successfully at Sat Oct 10 15:30:20 UTC 2026

[info] Running: ['airflow', 'tasks', 'test', 'university_etl_orchestration', 'show_student_name', '2026-01-01']
[info] Output: Submitted by: Mohammad Ayaan Sajid Shaikh
[info] Task show_student_name completed successfully.
```

---

## 8. Result
Successfully configured and deployed an Apache Airflow DAG managing an automated data engineering workflow, verified dependency resolution, and executed sequential tasks with complete log validation.

---

## 9. Learning Outcome
- Understood DAG concepts and dependency topologies in workflow automation.
- Learned how to author production Airflow DAGs using modern operator standards.
- Executed and tested individual task instances from CLI using `airflow tasks test`.
- Acquired hands-on experience in production data pipeline orchestration, scheduling, and error recovery.
