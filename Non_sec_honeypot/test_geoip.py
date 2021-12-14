import unittest
import geoip2.database

class TestIPAddress(unittest.TestCase):

    def test_address(self):
        reader = geoip2.database.Reader('/Users/admin/git/MSc_Project/SD_Project/GeoLite2-City_20211102/GeoLite2-City.mmdb')
        # test if geoip returns the correct countries
        response = reader.city('68.183.180.46')
        self.assertEqual(response.country.name, 'Singapore')
        response = reader.city('86.6.128.47')
        self.assertEqual(response.country.name, 'United Kingdom')
        response = reader.city('72.229.28.185')
        self.assertEqual(response.country.name, 'United States')
        response = reader.city('1.33.213.199')
        self.assertEqual(response.country.name, 'Japan')
        response = reader.city('1.0.1.0')
        self.assertEqual(response.country.name, 'China')
