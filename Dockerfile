FROM python:3.9-slim

RUN pip install pipenv
WORKDIR /code
ADD Pipfile ./
ADD Pipfile.lock ./
RUN pipenv install --system

ADD ./ ./
CMD ["python", "runserver.py"]
