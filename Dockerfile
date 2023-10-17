FROM python:3.10

RUN mkdir -p /home/app
COPY . /home/app

WORKDIR /home/app

RUN pip3 install virtualenv

RUN source venv/bin/activate