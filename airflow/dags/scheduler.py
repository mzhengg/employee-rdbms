import random
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

import mysql.connector

# login information
host = 'warehouse' # find in docker-compose.yml, line 5
port = '3306' # find in docker-compose.yml, line 13
user = os.getenv('MYSQL_USER') # get environmental variable
password = os.environ.get('MYSQL_PASSWORD') # get environmental variable
database = os.environ.get('MYSQL_DATABASE') # get environmental variable

# establish connection to mysql database
connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, auth_plugin='mysql_native_password')

# list of new employees
new_employees = []

# generates dummy employee information
def data_generator(n=10):
    # each new employee will have same information, except for SSN
    for i in range(n):
        first_name = 'Michael'
        middle_initial = 'B'
        last_name = 'Jordan'

        ssn = ''
        for i in range(9):
            ssn += str(random.randint(0, 9))
        
        birth_date = '1965-01-09'
        address = '731 Fondren, Houston, TX'
        sex = 'M'
        salary = '30000'
        super_ssn = '333445555'
        department_number = '5'

        # add new employee to list
        new_employee = [first_name, middle_initial, last_name, ssn, birth_date, address, sex, salary, super_ssn, department_number]
        new_employees.append(new_employee)

def insert_to_db(new_employees):
    cursor = connection.cursor()

    for i in range(len(new_employees)):
        data = (new_employees[i][0], new_employees[i][1], new_employees[i][2], new_employees[i][3], new_employees[i][4], new_employees[i][5], new_employees[i][6], new_employees[i][7], new_employees[i][8], new_employees[i][9])

        # add new employee to 'Employee' table
        cursor.execute("INSERT INTO EMPLOYEE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
        connection.commit()

    cursor.close()
    connection.close()

### DAG ###

default_args = {
    'owner': 'airflow',
    'start_date': '2022-1-1',
    'depends_on_past': False, # determines if task should be triggered if previous task hasn't succeeded
    'retries': 1 # number of retries that should be performed before failing the task
}

with DAG(
    dag_id = 'scheduler_dag',
    schedule_interval = '@weekly',
    default_args = default_args,
    catchup = False, # determines if DAG should run for any data interval not run since the last interval
    max_active_runs = 1, # total number of tasks that can run at the same time for a given DAG run
    tags = ['scheduler-dag']

) as dag:
    data_generator_task = PythonOperator(
        task_id = 'data_generator_task',
        python_callable = data_generator
    )

    insert_to_db_task = PythonOperator(
        task_id = 'insert_to_db_task',
        python_callablle = insert_to_db,
        op_kwargs = {
            'new_employees': new_employees
        }
    )

    data_generator_task >> insert_to_db_task