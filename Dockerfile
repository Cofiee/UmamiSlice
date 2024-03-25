FROM python:3.10.14-bookworm
COPY /flaskApp/flask-requirements.txt /
RUN pip install --no-cache-dir -r flask-requirements.txt

COPY workers/workers-requirements.txt /
RUN pip install --no-cache-dir -r workers-requirements.txt

WORKDIR /app