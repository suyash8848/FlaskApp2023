
FROM python:3.8-slim

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development 


COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app


RUN apt-get update && apt-get install -y libpq-dev



CMD ["flask", "run"]
