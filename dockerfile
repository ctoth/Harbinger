FROM sanicframework/sanic:LTS

ADD requirements.txt /srv/

RUN apk add --update --no-cache g++ gcc libxslt-dev libjpeg-turbo-dev

RUN pip3 install -r /srv/requirements.txt

COPY . /srv

EXPOSE 8888

ENTRYPOINT ["python" "/srv/harbinger.py"]
