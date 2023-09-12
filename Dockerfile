FROM python:3.11

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development 

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y libpq-dev

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
