import geoip2.database
import geohash

class GeoIPService:
    def __init__(self, db_path):
        """
        Initialize the GeoIPService with the path to the GeoLite2 City database.

        Args:
            db_path (str): Path to the GeoLite2-City.mmdb file.
        """
        self.db_path = db_path
        self.reader = None

    def load_database(self):
        """
        Load the GeoIP2 database.
        """
        try:
            self.reader = geoip2.database.Reader(self.db_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"GeoIP2 database not found at {self.db_path}")
        except Exception as e:
            raise Exception(f"Error loading GeoIP2 database: {e}")

    def lookup(self, ip_address):
        """
        Look up geographical information for a given IP address.

        Args:
            ip_address (str): The IP address to look up.

        Returns:
            dict: A dictionary containing geographical information.
        """
        if not self.reader:
            self.load_database()

        try:
            response = self.reader.city(ip_address)
            return {
                'continent': response.continent.name,
                'country': response.country.name,
                'state': response.subdivisions.most_specific.name,
                'city': response.city.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude,
                'postal_code': response.postal.code,
                'geohash': geohash.encode(response.location.latitude, response.location.longitude)
            }
        except geoip2.errors.AddressNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Error looking up IP address: {e}")

    def close(self):
        """
        Close the GeoIP2 database reader.
        """
        if self.reader:
            self.reader.close()

