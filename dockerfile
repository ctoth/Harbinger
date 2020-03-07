FROM python:3

ADD requirements.txt /srv/

RUN apt install g++ gcc libxslt-dev libjpeg-dev

RUN pip3 install -r /srv/requirements.txt

COPY . /srv

EXPOSE 8888

Cmd ["python3", "/srv/harbinger.py"]
