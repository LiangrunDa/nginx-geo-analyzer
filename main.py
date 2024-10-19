import yaml
from loguru import logger
from influx_srv import InfluxService
from geoip_srv import GeoIPService
from nginx_log_analyzer import NginxLogAnalyzer
import sys
import os

def load_config(config_path='config.yaml'):

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Override config with environment variables if they exist
    env_vars = {
        'INFLUX_HOST': 'influx_host',
        'INFLUX_PORT': 'influx_port',
        'NGINX_LOG': 'nginx_log',
        'INFLUX_USERNAME': 'influx_username',
        'INFLUX_PASSWORD': 'influx_password',
        'GEOIP2_DB': 'geoip2_db',
        'LOG_LEVEL': 'log_level'
    }

    for env_var, config_key in env_vars.items():
        if os.environ.get(env_var):
            config[config_key] = os.environ[env_var]

    return config

if __name__ == "__main__":
    config = load_config()
    logger.remove()
    logger.add(sys.stderr, level=config['log_level'].upper())
    logger.info(f"Log level set to: {config['log_level'].upper()}")
    logger.info("Current running parameters:")
    logger.info(f"InfluxDB Host: {config['influx_host']}")
    logger.info(f"InfluxDB Port: {config['influx_port']}")
    logger.info(f"Nginx Log Path: {config['nginx_log']}")
    logger.info(f"InfluxDB Username: {config['influx_username']}")
    logger.info(f"InfluxDB Password: {'*' * len(config['influx_password']) if config['influx_password'] else 'Not provided'}")

    client = InfluxService(config['influx_host'], config['influx_port'], config['influx_username'], config['influx_password'])
    client.create_client()
    logger.info(f"Successfully connected to InfluxDB")
    client.ensure_database_and_measurement()

    geoip_srv = GeoIPService(config['geoip2_db'])
    geoip_srv.load_database()
    logger.info(f"Successfully loaded GeoIP2 database")
    nginx_log_analyzer = NginxLogAnalyzer(config['nginx_log'], geoip_srv, client)
    nginx_log_analyzer.start()
