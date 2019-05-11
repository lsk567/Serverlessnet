From ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev
RUN apt-get install -y docker.io
RUN apt-get install -y libfribidi-bin

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "-u"]
CMD ["python_scripts/iot_python_script_node_1.py"]
