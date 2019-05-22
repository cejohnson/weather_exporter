FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r /requirements.txt

COPY ./weather_exporter /app/weather_exporter/
RUN chmod +x /app/weather_exporter/*

CMD /app/weather_exporter/exporter.py
