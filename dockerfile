FROM python:3-alpine

ADD requirements.txt /srv/

RUN apk add --update --no-cache g++ gcc libxslt-dev libjpeg-turbo-dev make

RUN pip3 install -r /srv/requirements.txt

COPY . /srv

EXPOSE 8888

Cmd ["python3" "/srv/harbinger.py"]
