import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from location.models import City
from location.weather_service import WeatherService
from todo_app.settings import PRIV

# Create your views here.

###############################################


def load_cities(request):
    """ Using the country name, get the object from the database
    and retrieve all cities that are related to that country.

    :param request: Http request object.
    :return: A template containing the filtered city objects.
    """

    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def load_weather(request):
    """ Using the city_id, get the object from the database
    and execute a request to open-weather api to retrieve the
    weather and location data stored in the City object.

    :param request: Http request object.
    :return: A Http Response object containing the colour code based on the weather data.
    """

    city_id = request.GET.get('city')
    city = City.objects.get(city_id=city_id)
    if city:

        url = 'http://api.openweathermap.org/data/2.5/weather'

        params = {
            'id': city.city_id,
            'units': 'metric',
            'appid': PRIV
        }

        response = requests.post(url, params=params)
        city.weather = response.json()

        weather_service = WeatherService(city)
        weather_service.init_service()

        city.save()

    return HttpResponse(
        json.dumps({"key": "background-color", "colour": city.temp_code}),
        content_type="application/json"
    )

