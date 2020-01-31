FROM python:3.8-alpine

COPY ./requirements.txt /app/requirements.txt
COPY migrations /app/migrations
COPY ./app /app/app
COPY ./config-sample /app/config.py
COPY ./helpers /app/helpers
COPY ./people.py /app/people.py
COPY entrypoint.sh /app/entrypoint
RUN sed -e "s/\r//g" /app/entrypoint > /app/entrypoint.sh
RUN chmod u+x /app/entrypoint.sh

WORKDIR /app

ENV FLASK_APP=people.py

RUN apk update && apk add postgresql-dev gcc sqlite python3-dev musl-dev &&\
    pip install -r requirements.txt

ENTRYPOINT [ "sh" ]
CMD [ "entrypoint.sh" ]
