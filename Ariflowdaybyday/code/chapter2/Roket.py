import json
import requests
import pathlib
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import bash_operator