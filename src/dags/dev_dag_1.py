import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.models.connection import Connection
from airflow.datasets import Dataset
from airflow.utils.edgemodifier import Label
from airflow.utils.task_group import TaskGroup

import pandas as pd 

"""
### My great DAG
"""

# SHOW DATABASES;
def fetch_records():
  sql_query = "SHOW DATABASES;"
  df = pd.read_sql(sql_query,Connection.get_connection_from_secrets('mysql_airflow').get_uri())
  print(df)
  return df

dev_dag = DAG(
    dag_id = 'dev_dag_1',
    start_date= airflow.utils.dates.days_ago(1),
    schedule_interval = None,
    tags=["custom"]
)
dev_dag.doc_md = __doc__
empty_op = EmptyOperator(task_id="task", dag=dev_dag)
bash_op = BashOperator(task_id="hello_world", 
                        bash_command="echo $MY_VAR",
                        env={"MY_VAR": "Hello World"},
                        dag=dev_dag
                    )
bash_op.doc_md = """\
#Title"
Here's a [url](www.airbnb.com)
"""
py_op = PythonOperator(task_id='db_identification', 
                        python_callable= lambda: print(Connection.get_connection_from_secrets('mysql_airflow').get_uri()), 
                        dag = dev_dag
                    )
db_op = PythonOperator(task_id='db_operation',
                        python_callable=fetch_records,
                        outlets = [Dataset('dataframe://Database List')],
                        dag = dev_dag
                    )
tasks = []
for _ , r in fetch_records().iterrows():
  t = EmptyOperator(task_id=r['Database'])
  tasks.append(t)

# [START howto_task_group_section_1]
with TaskGroup("section_1", tooltip="Tasks for section_1", dag=dev_dag) as section_1:
    task_1 = EmptyOperator(task_id="task_1",dag=dev_dag)
    task_2 = BashOperator(task_id="task_2", bash_command="echo 1", dag=dev_dag)
    task_3 = EmptyOperator(task_id="task_3", dag=dev_dag)

    task_1 >> [task_2, task_3]

bash_op >> empty_op >> section_1 >> py_op >> db_op >> Label('Process respective databases') >> tasks