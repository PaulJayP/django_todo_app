from location.tests.api.test_weather_api_mixin import TestWeatherApiMixin
from django.test import Client
from django.urls import reverse


class ViewLoadCitiesTestCase(TestWeatherApiMixin):

    def setUp(self):
        super().setUp()

    def test_get_load_cities_success(self):

        for obj in self.location_list:
            country = obj['country']

            client = Client()

            response = client.get(
                reverse('load_cities'), data={'country': country.pk}
            )

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'city_dropdown_list_options.html')

            for city in response.context['cities']:
                self.assertEqual(city, obj['city'])

