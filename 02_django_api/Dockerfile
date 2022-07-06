FROM python:latest

ENV PYTHONUNBUFFERED  1

RUN mkdir /02-django-api
WORKDIR /02-django-api
COPY requirements.txt /02-django-api/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD ./02-django-api

EXPOSE 8000

CMD [ "python", "./manage.py runserver localhost:8000" ]