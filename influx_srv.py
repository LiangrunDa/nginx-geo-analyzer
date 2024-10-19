from influxdb import InfluxDBClient
import sys

class InfluxService:
    def __init__(self, host, port, username=None, password=None):
        """
        Initialize the InfluxDBManager with connection details.

        Args:
            host (str): The InfluxDB host address.
            port (int): The InfluxDB port number.
            username (str, optional): The InfluxDB username. Defaults to None.
            password (str, optional): The InfluxDB password. Defaults to None.
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def create_client(self):
        """
        Create and return an InfluxDB client. Exit if connection fails.

        Returns:
            InfluxDBClient: An instance of InfluxDBClient.
        """
        try:
            if self.username and self.password:
                self.client = InfluxDBClient(host=self.host, port=self.port, username=self.username, password=self.password)
            else:
                self.client = InfluxDBClient(host=self.host, port=self.port)
            
            # Test the connection
            self.client.ping()
            return self.client
        except Exception as e:
            print(f"Failed to connect to InfluxDB: {e}", file=sys.stderr)
            sys.exit(1)

    def ensure_database_and_measurement(self):
        """
        Check if the 'nginx-geo-analyzer' database and 'geo-log' measurement exist.
        If they don't exist, create them.
        """
        try:
            if not self.client:
                raise Exception("InfluxDB client not created. Call create_client() first.")

            # Check if the database exists
            databases = self.client.get_list_database()
            if not any(db['name'] == 'nginx-geo-analyzer' for db in databases):
                self.client.create_database('nginx-geo-analyzer')
                print("Created 'nginx-geo-analyzer' database.")

            # Switch to the database
            self.client.switch_database('nginx-geo-analyzer')

            # Check if the measurement exists
            measurements = self.client.get_list_measurements()
            if not any(measurement['name'] == 'geo-log' for measurement in measurements):
                # Create an empty point to initialize the measurement
                json_body = [
                    {
                        "measurement": "geo-log",
                        "fields": {
                            "init": True
                        }
                    }
                ]
                self.client.write_points(json_body)
                print("Initialized 'geo-log' measurement.")

        except Exception as e:
            print(f"Error ensuring database and measurement: {e}", file=sys.stderr)
            sys.exit(1)
