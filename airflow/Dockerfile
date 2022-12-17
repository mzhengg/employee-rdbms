# base image
FROM apache/airflow:2.2.3

# set user to root to get permissions
USER root

# update apt-get
RUN apt-get update

# install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt