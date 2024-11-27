import mariadb
from math import sin, cos, sqrt, atan2, radians
from connector.AbstractDbConnector import AbstractDbConnector


class MariaDbConnector(AbstractDbConnector):

    def __init__(self, driver, server, database, user, pw, port):
        super().__init__(driver, server, database, user, pw, port)
        self.connection = mariadb.connect(host=server, database=database, user=user, password=pw, port=int(port))
        self.global_cursor = self.connection.cursor()

    def get_lat_long_coordinates_from_db(self, country_name, city_name):
        try:
            result = []

            country_name = str(country_name).replace("_", " ")
            city_name = str(city_name).replace("_", " ")

            if country_name is not None:
                self.global_cursor.execute("SELECT Cc2 FROM GeoCountry WHERE Name = ? OR Alternatename = ?;", (country_name, country_name))
                cc2 = self.global_cursor.fetchone()
                if cc2 is not None:
                    self.global_cursor.execute("SELECT Asciiname, Latitude, Longitude, Featurecode, Featureclass, Countrycode FROM GeoEntity WHERE AsciiName = ? AND Countrycode = ?;", (city_name, cc2[0]))
                else:
                    self.global_cursor.execute("SELECT Asciiname, Latitude, Longitude, Featurecode, Featureclass, Countrycode  FROM GeoEntity WHERE AsciiName = ? OR Name = ?;", (city_name, city_name))
            else:
                self.global_cursor.execute("SELECT Asciiname, Latitude, Longitude, Featurecode, Featureclass, Countrycode  FROM GeoEntity WHERE AsciiName = ? OR Name = ?;", (city_name, city_name))

            self.extract_lines_from_db(result)

            if len(result) == 0:
                return self.try_with_alternate_name(city_name, cc2)

            return result

        except mariadb.Error as e:
            print("Error while connecting to MariaDb", e)
        finally:
            print("MariaDb connection is closed")

    def extract_lines_from_db(self, result):
        for (Asciiname, Latitude, Longitude, Featurecode, Featureclass, Countrycode) in self.global_cursor:
            lat = Latitude
            long = Longitude
            city = Asciiname
            country = Countrycode
            result.append({"Entity": city, "Country": country, "Latitude": lat, "Longitude": long, "FeatureClass": Featureclass, "FeatureCode": Featurecode, "Score": 0.0})

    def get_capital(self, country):
        result = None
        if country is not None:
            self.global_cursor.execute('SELECT Name FROM GeoCapital WHERE Land = ? ;', [country])
            if self.global_cursor.arraysize > 0:
                return self.global_cursor.fetchone()
        return result

    def get_distance(self, entity1, entity2):
        # Approximate radius of earth in km
        R = 6373.0

        lat1 = radians(entity1[0])
        lon1 = radians(entity1[1])
        lat2 = radians(entity2[0])
        lon2 = radians(entity2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        print("Result: ", distance)
        return distance

    def try_with_alternate_name(self, city_name, country_code):
        if country_code is not None:
            self.global_cursor.execute("SELECT Geonameid FROM GeoEntityAll WHERE Alternatename = ? AND Countrycode = ?;", (city_name, country_code[0]))
        else:
            self.global_cursor.execute("SELECT Geonameid FROM GeoEntityAll WHERE Alternatename = ?;", [city_name])
        result = []
        ids = []

        for Geonameid in self.global_cursor:
            ids.append(Geonameid)

        for Geonameid in ids:
            self.global_cursor.execute("SELECT Asciiname, Latitude, Longitude, Featurecode, Featureclass, Countrycode FROM GeoEntity WHERE Geonameid = ?;", Geonameid)
            self.extract_lines_from_db(result)

        return result
