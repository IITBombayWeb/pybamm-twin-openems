FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY ./pymodbus-fastapi-simulation/pyproject.toml ./pymodbus-fastapi-simulation/poetry.lock* /code/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
COPY ./pymodbus-fastapi-simulation/pymodbus_fastapi_simulation /code/pymodbus_fastapi_simulation

COPY ./pymodbus-fastapi-simulation/entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]
