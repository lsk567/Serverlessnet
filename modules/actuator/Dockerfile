FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install -y curl iproute2

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY ./state.txt /app/state.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# Containernet neglects the two lines below somehow
ENTRYPOINT [ "python" ]
CMD [ "actuator.py" ]