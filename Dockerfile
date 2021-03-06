FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv \
    && pipenv install --system
COPY . /code/
RUN python manage.py migrate
EXPOSE 8000