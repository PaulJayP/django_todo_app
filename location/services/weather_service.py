from location.models.city_model import City


class WeatherService:

    weather_colour_code = {
        "cold": "blue",
        "rain": "blue",
        "warm": "yellow",
        "clouds": "orange",
        "hot": "red",
        "clear": "red"
    }

    def __init__(self, city_obj: City):
        self.the_city = city_obj
        self.the_city_weather = city_obj.weather

    def init_service(self):
        temp = 0
        weather_colour_resp = self.get_weather_code()
        temp_colour_resp, temp = self.get_temp_code()

        colour_resp = weather_colour_resp
        if not weather_colour_resp:
            colour_resp = temp_colour_resp

        self.assign_weather_data(colour_resp, temp)

    def get_weather_code(self):
        city_weather_obj = self.the_city_weather.get('weather')[0]
        weather_code = self.weather_colour_code.get(city_weather_obj['main'].lower(), None)
        return weather_code

    def get_temp_code(self):

        city_weather_main = self.the_city_weather.get('main')
        temp = city_weather_main.get('temp')

        temp_code = None
        if temp > 30:
            temp_code = self.weather_colour_code['hot']
        elif temp > 20:
            temp_code = self.weather_colour_code['warm']
        else:
            temp_code = self.weather_colour_code['cold']

        return temp_code, temp

    def assign_weather_data(self, temp_code, temp):

        self.the_city.temp_code = temp_code
        self.the_city.temperature = temp
