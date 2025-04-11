FROM apache/airflow
ADD requirements.txt .
ADD airflow.cfg .
ADD webserver_config.py .
ADD src/config/connections/connections.json /opt/airflow/config/connections.json
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt