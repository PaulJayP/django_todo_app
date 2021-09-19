from unittest import mock
from unittest.mock import Mock

from location.tests.api.test_weather_api_mixin import TestWeatherApiMixin
from django.test import Client
from django.urls import reverse


class ViewLoadWeatherTestCase(TestWeatherApiMixin):

    def setUp(self):
        super().setUp()

    @mock.patch('location.views.WeatherService')
    @mock.patch('requests.post')
    def test_get_load_weather_success(self, mock_post, mock_weather_service):

        mock_post.return_value = Mock(status_code=201, json=lambda: {"data": {"id": "test"}})
        mock_weather_service.return_value = Mock()
        mock_weather_service.init_service.return_value = None

        for obj in self.location_list:
            city = obj['city']

            client = Client()

            response = client.get(
                reverse('load_weather'), data={'city': city.city_id}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"key": "background-color", "colour":  city.temp_code})
