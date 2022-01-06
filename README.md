# Pet Projects API

 [![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/diogo-alves/pet-projects-api/blob/main/LICENSE) [![tests](https://github.com/diogo-alves/pet-projects-api/actions/workflows/tests.yml/badge.svg)](https://github.com/diogo-alves/pet-projects-api/actions/workflows/tests.yml) [![codecov](https://codecov.io/gh/diogo-alves/pet-projects-api/branch/main/graph/badge.svg)](https://codecov.io/gh/diogo-alves/pet-projects-api)

An API to aggregate personal projects.


## Features

- [x] CRUD operations
- [x] Authentication with JWT
- [x] Layered Architecture
- [x] Custom exceptions and handlers
- [x] Database migrations with Alembic
- [x] Management commands with Typer
- [x] Dockenized app running PostgreSQL and pgAdmin
- [x] Tests with Pytest
- [x] Continuous Integration with Github Actions
- [x] Continuous Deployment at Heroku


## Live Preview

See the [live preview](https://pet-projects-api.herokuapp.com/docs) deployed at Heroku.
[![pet-projects-api](https://i.imgur.com/haTcMnI.png)](https://pet-projects-api.herokuapp.com/docs)


## Getting Started

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker-compose](https://docs.docker.com/compose/install/)
- [Python 3.10.1](https://www.python.org/downloads/release/python-3101/)
- [Poetry](https://python-poetry.org/docs/#installation)


### Setup

1. Clone this repository:

```shell
git clone git@github.com:diogo-alves/pet-projects-api.git
```

2. Go to the project directory:

```shell
cd pet-projects-api
```

3. Install the python dependencies:

```shell
poetry install
```

4. Create an ```.env```¹ file based on ```.env.example``` . Generate the SECRET_KEY with this utility command:

```shell
poetry run python manage.py utils gensecretkey
```
¹ NOTE: <small>By running the app locally, you can set DATABASE_URL to use SQLite without having to install a database system.</small>

## Run Locally

1. Run server
```shell
poetry run uvicorn app.main:app --reload
```

2. Run database migrations:
```shell
poetry run alembic upgrade head
```

## Run With docker-compose

1. Start services (Web server, PostgreSQL and pgAdmin)
```shell
docker-compose up -d
```

2. Run database migrations:
```shell
docker-compose exec web alembic upgrade head
```

## View in Browser

- API: [```http://localhost:8000/docs```](http://localhost:8000/docs)
- pgAdmin: [```http://localhost:5050```](http://localhost:5050) (only running with docker)


## Run Tests

```shell
poetry run pytest --cov=app
```

## Management Commands

To see all commands type:
```shell
poetry run python manage.py --help
```

## API Documentation

- Swagger UI: [```(http://localhost:8000/docs/```](http://localhost:8000/docs/)
- Redoc: [```http://localhost:8000/redoc```](http://localhost:8000/redoc)


## License

This project is under the terms of the [MIT](./LICENSE) license.
