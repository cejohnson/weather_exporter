# weather_exporter

A very simplified fork of weather_exporter which uses a `config.json` file that looks like this:

```json
{
	"dark_sky_api_key": "<key>",
	"locations": [{
			"name": "Staten Island",
			"latitude": 40.5773,
			"longitude": -74.1505
		},
		{
			"name": "JFK International Airport",
			"latitude": 40.6421,
			"longitude": -73.7810
		}
	]
}
```

to allow for more precise weather readings. Just go to Google Maps (or wherever) to find the lat/long of your location(s).

It has been updated to use Python 3, and most of the options in the original project have been removed.

## Usage

#### Build container
```bash
$ docker build -t weather-exporter .
```

#### Edit `config.json`
Add your Dark Sky API key and locations.

#### Run container
```bash
$ docker-compose up -d
```

#### Prometheus Endpoint

http://localhost:9265

#### Prometheus config
```yaml
scrape_configs:

  - job_name: weather_exporter
    metrics_path: /
    static_configs:

      - targets:
        - '127.0.0.1:9265'
        labels:
          alias: 'weather-exporter'
 ```
