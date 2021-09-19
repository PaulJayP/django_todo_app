import random
import string
import uuid
from django.test import TestCase

from django.test.testcases import SerializeMixin

from location.models.city_model import City
from location.models.country_model import Country


class TestWeatherApiMixin(SerializeMixin, TestCase):

    lockfile = __file__

    def setUp(self):

        self.location_list = []

        temp_code = ['red', 'blue', 'orange']
        temp = [10, 20, 30]

        for x in range(5):
            test_country = Country.objects.create(name="test_country [{0}]".format(str(uuid.uuid4())[:25]))
            test_city = City.objects.create(
                city_id=str(uuid.uuid4()),
                name=''.join(random.choice(string.ascii_letters) for i in range(100)),
                country=test_country,
                state=''.join(random.choice(string.ascii_letters) for i in range(100)),
                coord={"lon": 01.111111, "lat": 01.111111},
                weather={'test_weather': 'not null'},
                temp_code=random.choice(temp_code),
                temperature=random.choice(temp)
            )

            self.location_list.append(
                {
                    'country': test_country,
                    'city': test_city
                }
            )