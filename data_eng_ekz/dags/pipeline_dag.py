import os
import datetime
# Task here is PythonOperator (airflow.providers.standard.operators.python)
from airflow.decorators import dag, task

# We are in /opt/airflow/{dags,etl} directory, so we need to add module search `..`
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import CONFIG

def notify_failure(context):
    print(f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")

default_args = {
    "depends_on_past": False,
    "retries": 5,
    "retry_delay": datetime.timedelta(minutes=1),
    "on_failure_callback": notify_failure,
    "start_date": datetime.datetime(2000, 1, 1),
}

@dag(
    dag_id="pipeline_dag",
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args=default_args
)
def dag_pipeline():   
    @task(task_id="download")
    def download(ds=None, **kwargs):
        import etl.download as mod
        mod.download_and_save(CONFIG["raw_data_filepath"])
    
    @task(task_id="preproces")
    def preprocess(ds=None, **kwargs):
        import etl.preprocess as mod
        mod.preprocess(CONFIG["raw_data_filepath"], CONFIG["data_filepath"])

    @task(task_id="train")
    def train(ds=None, **kwargs):
        import etl.train as mod
        mod.train(CONFIG["data_filepath"], CONFIG["model_filepath"])

    @task(task_id="evaluate")
    def evaluate(ds=None, **kwargs):
        import etl.evaluate as mod
        mod.evaluate(CONFIG["data_filepath"], CONFIG["model_filepath"], CONFIG["metrics_path"])

    @task(task_id="upload")
    def upload(ds=None, **kwargs):
        import etl.upload as mod
        mod.upload(CONFIG["model_filepath"], CONFIG["metrics_path"])

    download() >> preprocess() >> train() >> evaluate() >> upload()

dag_pipeline()
