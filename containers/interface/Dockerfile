# base image
FROM python:3.9.5

# create directory 'main' in container and set as work directory
WORKDIR /main

# copy code into container
COPY ./containers/interface/interface.py interface.py

# copy file into container
COPY ./containers/interface/requirements.txt requirements.txt

# install python dependencies
RUN pip install -r requirements.txt

# just to keep the container running
ENTRYPOINT ["tail", "-f", "/dev/null"]