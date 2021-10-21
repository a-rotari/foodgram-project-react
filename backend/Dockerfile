FROM python:3.8.5

WORKDIR /code
COPY requirements.txt /code
COPY ../data/ingredients.json /code
RUN pip install -r /code/requirements.txt
COPY . /code
