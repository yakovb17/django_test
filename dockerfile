FROM python:3.8.15-alpine3.16

WORKDIR /pcentra_test

COPY . .

RUN apk update --no-cache \
    && apk add build-base postgresql-dev libpq --no-cache --virtual .build-deps 
RUN apk add postgresql-libs libpq

RUN pip install -r requirements.txt

EXPOSE 8000

# CMD [ "python", "manage.py", "runserver" ]