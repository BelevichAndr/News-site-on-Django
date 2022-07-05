FROM python:3.8.5-alpine

WORKDIR .
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    zlib-dev

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .. .

CMD python manage.py runserver 0.0.0.0:8000



