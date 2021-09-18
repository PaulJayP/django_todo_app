import random
import string

from location.models.country_model import Country
from location.tests.models.test_location_models_mixin import TestLocationModelsMixin


class CountryModelTestCase(TestLocationModelsMixin):

    def setUp(self):
        super().setUp()

    def test_name_label(self):
        countries = Country.objects.all()

        for country in countries:
            name_label = country._meta.get_field('name').verbose_name
            self.assertEqual(name_label, 'name')

    def test_return_string(self):
        countries = Country.objects.all()

        for country in countries:
            name_label = country._meta.get_field('name').verbose_name
            self.assertEqual(str(country), country.name)

    def test_add_new_object_exceed_max_field_name_length(self):

        rand_name_max = ''.join(random.choice(string.ascii_letters) for i in range(51))

        error_raised = False
        try:
            country = Country.objects.create(name=rand_name_max)
        except Exception as err:
            error_raised = True
        self.assertEqual(error_raised, True)

    def test_add_unique_field_names(self):

        unique_name = 'unique'

        error_raised = False
        try:
            country_1 = Country.objects.create(name=unique_name)
            country_2 = Country.objects.create(name=unique_name)
        except Exception as err:
            error_raised = True
        self.assertEqual(error_raised, True)