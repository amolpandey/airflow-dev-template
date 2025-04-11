# Airflow + MySQL Development Template 

This codebase is prepared to illustrate the functionalities provided by the airflow for development and learning. 

## Refrence Article: 

[Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#before-you-begin)

## Setup of local development

`python -m venv .aflw`

`.\.aflw\Scripts\activate.ps1`

`pip install apache-airflow pandas`

`python.exe -m pip install --upgrade pip`

## Download the Docker Compose File

`curl 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml' -OutFile docker-compose.yaml`

`Rename-Item .\docker-compose.yaml -NewName compose.yaml`

## Intialize the Airflow Container and Startup the services

`docker compose build`

`docker compose up airflow-init`

`docker compose up`

OR

`docker compose --profile flower up`

## Copy the airflow.cfg file (from the webserver container)

`docker cp a14983fa6945:/opt/airflow/airflow.cfg ./src/config/airflow.cfg`

## Create a new file to trigger the DAG
`New-Item -Path ./src/data/demo.txt -ItemType File`

## Import the Connection from the JSON file

`docker exec airflow-dev-airflow-webserver-1 airflow connections import /opt/airflow/config/connections.json`
