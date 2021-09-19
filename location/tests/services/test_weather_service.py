import random
import string
import uuid

from django.test import TestCase

from location.models.city_model import City
from location.models.country_model import Country
from location.services.weather_service import WeatherService


class WeatherServiceTestCase(TestCase):

    def setUp(self):
        self.test_country = Country.objects.create(name="test_country [{0}]".format(str(uuid.uuid4())[:25]))
        self.test_city = City.objects.create(
            city_id=str(uuid.uuid4()),
            name=''.join(random.choice(string.ascii_letters) for i in range(100)),
            country=self.test_country,
            state=''.join(random.choice(string.ascii_letters) for i in range(100)),
            coord={"lon": 01.111111, "lat": 01.111111},
            weather={
                'weather': [
                    {
                        'main': 'Clouds'
                    }
                ],
                'main': {
                    'temp': 10
                }
            }
        )

    def test_weather_service_with_base_city_obj_clouds_10(self):

        weather_service = WeatherService(city_obj=self.test_city).init_service()
        self.assertEqual(self.test_city.temp_code, 'orange')
        self.assertEqual(self.test_city.temperature, 10)

    def test_weather_service_with_city_obj_clear_10(self):
        self.test_city.weather['weather'][0]['main'] = 'Clear'

        weather_service = WeatherService(city_obj=self.test_city).init_service()

        self.assertEqual(self.test_city.temp_code, 'red')
        self.assertEqual(self.test_city.temperature, 10)

    def test_weather_service_with_city_obj_rain_10(self):
        self.test_city.weather['weather'][0]['main'] = 'Rain'

        weather_service = WeatherService(city_obj=self.test_city).init_service()

        self.assertEqual(self.test_city.temp_code, 'blue')
        self.assertEqual(self.test_city.temperature, 10)

    def test_weather_service_with_city_obj_temp_10_cold(self):
        self.test_city.weather['weather'][0]['main'] = 'Unknown'
        self.test_city.weather['main']['temp'] = 10

        weather_service = WeatherService(city_obj=self.test_city).init_service()

        self.assertEqual(self.test_city.temp_code, 'blue')
        self.assertEqual(self.test_city.temperature, 10)

    def test_weather_service_with_city_obj_temp_20_warm(self):
        self.test_city.weather['weather'][0]['main'] = 'Unknown'
        self.test_city.weather['main']['temp'] = 20

        weather_service = WeatherService(city_obj=self.test_city).init_service()

        self.assertEqual(self.test_city.temp_code, 'yellow')
        self.assertEqual(self.test_city.temperature, 20)

    def test_weather_service_with_city_obj_temp_30_hot(self):
        self.test_city.weather['weather'][0]['main'] = 'Unknown'
        self.test_city.weather['main']['temp'] = 30

        weather_service = WeatherService(city_obj=self.test_city).init_service()

        self.assertEqual(self.test_city.temp_code, 'red')
        self.assertEqual(self.test_city.temperature, 30)
