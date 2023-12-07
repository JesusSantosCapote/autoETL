FROM python:3.10

RUN mkdir -p /home/app
WORKDIR /home/app

COPY ./requirements.txt /home/app/requirements.txt
RUN pip install -r /home/app/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT "/entrypoint.sh"
