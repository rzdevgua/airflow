# import libraries
# import requests,airflow and json
import json
import requests
import pathlib
import requests.exceptions as requests_exceptions
import airflow as airflow 
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

dag = DAG(
    dag_id="download_rocket_launches",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
    tags=["example"]
)

dowlnoad_rocket_launches = BashOperator(
    task_id="download_rocket_launches",
    bash_command="curl -o /tmp/rocket_launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    dag=dag,
)

def _get_pictures():
    # Ensure the /tmp directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    # Download all pictures in launches.json
    with open("/tmp/rocket_launches.json") as f:
        data = json.load(f)
        image_urls = [launch["image"] for launch in data["results"] ]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"coudn't connect to {image_url}")
    _get_pictures = PythonOperator(
        task_id="get_pictures",
        python_callable=_get_pictures,
        dag=dag,
    )

    notify = bash_operator(
        task_id="notify",
        bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
        dag=dag,
    )

    dowlnoad_rocket_launches >> _get_pictures >> notify