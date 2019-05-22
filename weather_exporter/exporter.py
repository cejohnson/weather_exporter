import json
import logging
import os
import requests
import re
import time

from prometheus_client import start_http_server, Gauge

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class WeatherExporter:
    def __init__(self, config):
        self.config = config
        self.gauges = {}
        self.weather = {}

    def get_weather(self, location):
        url = f'https://api.darksky.net/forecast/{config["dark_sky_api_key"]}/{location["latitude"]},{location["longitude"]}'
        params = {
            'units': config.get('units', 'us')
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            self.weather[location['name']] = response.json()
        except requests.exceptions.RequestException as e:
            logger.error('Error while querying Dark Sky API: %s', e)
            if e.response is not None:
                logger.error('Response: %s', e.response.text)

    def to_underscore(self, str):
        return re.sub("([A-Z])", "_\\1", str).lower().lstrip("_")

    def add_gauge(self, latest_weather):
        for key, value in latest_weather.items():
            name = self.to_underscore(key)
            self.gauges[key] = Gauge(f'weather_{name}', f'Current Weather {name}', ['location'])

    def report_metrics(self, location):
        name = location['name']
        self.weather[name] = {}
        self.get_weather(location)
        latest_weather = self.weather[name]
        try:
            self.add_gauge(latest_weather['currently'])
        except Exception:
            pass

        try:
            for key, value in latest_weather['currently'].items():
                if type(value) == int or type(value) == float:
                    self.gauges[key].labels(name).set(value)
        except Exception:
            pass


if __name__ == "__main__":
    config_file = os.environ.get('CONFIG_FILE', '/etc/weather_exporter/config.json')
    with open(config_file, 'r') as cf:
        config = json.load(cf)

    exporter = WeatherExporter(config)
    start_http_server(os.environ.get('PORT', 9265))
    while True:
        for location in config['locations']:
            exporter.report_metrics(location)
        try:
            time.sleep(os.environ.get('SCRAPE_INTERVAL', 600))
        except KeyboardInterrupt:
            break
