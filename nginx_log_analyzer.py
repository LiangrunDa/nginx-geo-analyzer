import time
from pygtail import Pygtail
import re
from datetime import datetime
from loguru import logger

class NginxLogAnalyzer:
    def __init__(self, log_file, geoip_service, influx_service):
        self.log_file = log_file
        self.geoip_service = geoip_service
        self.influx_service = influx_service
        self.log_pattern = re.compile(
            r'(?P<ip>[\d.]+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/\d\.\d" (?P<status>\d+) (?P<bytes_sent>\d+) "(?P<referer>.*?)" "(?P<user_agent>.*?)"'
        )

    def parse_log_line(self, line):
        match = self.log_pattern.match(line)
        if match:
            return match.groupdict()
        return None

    def process_log_entry(self, entry):
        if entry:
            logger.debug(f"Processing log entry: {entry}")
            ip_address = entry['ip']
            timestamp = datetime.strptime(entry['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
            
            geo_info = self.geoip_service.lookup(ip_address)
            logger.debug(f"Geo info: {geo_info}")
            
            if geo_info:
                json_body = [{
                    "measurement": "geo-log",
                    "time": timestamp.isoformat(),

                    "tags": {
                        "ip": ip_address,
                        "method": entry['method'],
                        "path": entry['path'],
                        "status": entry['status'],
                        "referer": entry['referer'],
                        "user_agent": entry['user_agent'],
                        "continent": geo_info.get('continent', ''),
                        "country": geo_info.get('country', ''),
                        "state": geo_info.get('state', ''),
                        "city": geo_info.get('city', ''),
                        "bytes_sent": int(entry['bytes_sent']),
                        "latitude": float(geo_info.get('latitude', 0)),
                        "longitude": float(geo_info.get('longitude', 0)),
                        "postal_code": geo_info.get('postal_code', ''),
                        "geohash": geo_info.get('geohash', ''),
                    },
                    "fields": {
                        "count": 1
                    }
                }]
                
                self.influx_service.client.write_points(json_body)
            else:
                logger.warning(f"No geo information found for IP: {ip_address}")

    def start(self):
        logger.info(f"Starting to analyze Nginx log file: {self.log_file}")
        while True:
            for line in Pygtail(self.log_file, read_from_end=True):
                entry = self.parse_log_line(line)
                self.process_log_entry(entry)
            time.sleep(1)  # Wait for 1 second before checking for new lines again



