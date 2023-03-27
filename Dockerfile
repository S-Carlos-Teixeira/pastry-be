FROM python:3

ARG ENV_FILE=.env
ENV ENV_FILE=${ENV_FILE}

WORKDIR /app
COPY . .

RUN pip3 install pipenv
RUN pipenv install

ENTRYPOINT  pipenv run flask run --host 0.0.0.0 --port 4000

EXPOSE 4000

# pipenv run python seed.py &&