FROM python:3.8.5-slim AS container-image

RUN apt-get update && apt-get install --no-install-recommends -y \
    gunicorn \
    curl \
    postgresql \
    gcc \
    sqlite \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM container-image

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY migrations /app/migrations
COPY ./app /app/app
COPY ./seed /app/seed
COPY ./helpers /app/helpers
COPY ./people.py /app/people.py

WORKDIR /app

ENV FLASK_APP=people.py

# /dev/shm removes the deadlock waiting for a file to write to
# --accesslog-file=-   ---> write to standard out
# --log-file=-   ---> write errors to standard err
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=2 --threads=2 --worker-tmp-dir /dev/shm --access-logfile=- --log-file=-"

CMD ["gunicorn", "people:app"]
