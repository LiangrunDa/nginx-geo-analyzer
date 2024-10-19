# nginx-geo-analyzer

A non-intrusive Nginx log analyzer with geographical insights.

## Overview

This project provides a solution for analyzing Nginx access logs with geographical information without requiring modifications to your Nginx configuration. It draws inspiration from [geoip2influx](https://github.com/GilbN/geoip2influx) for dashboard design but offers a key advantage: it doesn't require the installation of additional Nginx modules like [ngx_http_geoip2_module](https://github.com/leev/ngx_http_geoip2_module). 

Additionally, we provide an example Grafana dashboard. Of course, you can design or modify the dashboard yourself - you just need to add InfluxDB as a data source.

## Key Features

- Analyzes standard Nginx access logs without any modifications to Nginx
- Provides geographical insights based on IP addresses in the logs
- Stores analyzed data in InfluxDB for easy visualization
- Compatible with existing Nginx setups
- Example Grafana dashboard included

## Prerequisites

- Conda or Python 3.8
- InfluxDB 1.8
- Grafana 11.2.2
- GeoLite2-City.mmdb, provided by [MaxMind](https://www.maxmind.com/en/geolite2/signup). Please place it in the `geodb` directory.
- Nginx with default access log format, for example:

```
access_log  /var/log/nginx/access.log;
```

## Usage

### Setup environment

If you use Conda, you can create an environment with the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

Otherwise, you can install the dependencies manually using `pip`:

```bash
pip install -r requirements.txt
```

Edit the `config.yaml` file to match your environment. For example:

```yaml
influx_host: localhost
influx_port: 8086
nginx_log: /var/log/nginx/access.log
influx_username: null
influx_password: null
geoip2_db: ./geodb/GeoLite2-City.mmdb
log_level: INFO
```

- `influx_host`: The hostname or IP address of your InfluxDB server. Default is 'localhost'.
- `influx_port`: The port number on which InfluxDB is running. Default is 8086.
- `nginx_log`: The full path to your Nginx access log file. Default is '/var/log/nginx/access.log'.
- `influx_username`: The username for InfluxDB authentication. Set to null if authentication is not required.
- `influx_password`: The password for InfluxDB authentication. Set to null if authentication is not required.
- `geoip2_db`: The path to your GeoLite2-City.mmdb file. Default is './geodb/GeoLite2-City.mmdb'.
- `log_level`: The logging level for the application. Default is 'INFO'.

### Run

Then you can run the script by:

```bash
python main.py
```

### Grafana dashboard

You can use the [`dashboard.json`](https://github.com/liangrunda/nginx-geo-analyzer/blob/main/grafana/dashboard.json) file to import the dashboard into Grafana. 


## Docker Usage

If you prefer using Docker, you can run the container with the following command:

```bash
docker run -d \
  -e INFLUX_HOST=<your_influx_host> \
  -e INFLUX_PORT=<your_influx_port> \
  -e INFLUX_USERNAME=<your_influx_username> \
  -e INFLUX_PASSWORD=<your_influx_password> \
  -v <your_geodb_dir>:/app/geodb \
  -v <your_nginx_log_dir>:/var/log/nginx \
  nginx-geo-analyzer
```

## How It Works

nginx-geo-analyzer reads your default Nginx access logs, using a python script processes the IP addresses to obtain geographical information, and stores the results in InfluxDB. The GeoIP2 database is provided by [MaxMind](https://www.maxmind.com/) and it is only needed in the python script (instead of the Nginx module).
