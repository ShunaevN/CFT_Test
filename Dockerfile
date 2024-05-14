FROM python:3.12

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

RUN chmod a+x docker/*.sh
