FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system --deploy --dev

RUN groupadd -r django && useradd -r --uid 1000 --create-home -g django django
ADD . /app

WORKDIR /app
