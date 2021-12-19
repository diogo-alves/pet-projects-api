FROM python:3.10.1-slim as requirements

WORKDIR /tmp

RUN pip install poetry

COPY poetry.lock pyproject.toml /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY --from=requirements /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
