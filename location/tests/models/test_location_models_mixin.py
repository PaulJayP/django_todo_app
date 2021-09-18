import random
import uuid

from django.test.testcases import SerializeMixin
from django.test import TestCase

from location.models.city_model import City
from location.models.country_model import Country


class TestLocationModelsMixin(SerializeMixin, TestCase):

    lockfile = __file__

    def setUp(self):

        self.location_list = []

        temp_code = ['red', 'blue', 'orange']
        temp = [10, 20, 30]

        for x in range(5):
            test_country = Country.objects.create(name="test_country [{0}]".format(str(uuid.uuid4())[:25]))
            test_city = City.objects.create(
                country=test_country,
                city_id=str(uuid.uuid4()),
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