import random
import string

from location.models.city_model import City
from location.models.country_model import Country
from location.tests.models.test_location_models_mixin import TestLocationModelsMixin


class CityModelTestCase(TestLocationModelsMixin):

    def setUp(self):
        super().setUp()

    def test_city_id_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        city_id_label = city_obj._meta.get_field('city_id').verbose_name
        self.assertEqual(city_id_label, 'city id')

    def test_name_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        name_label = city_obj._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'name')

    def test_country_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        country_label = city_obj._meta.get_field('country').verbose_name
        self.assertEqual(country_label, 'country')

    def test_state_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        state_label = city_obj._meta.get_field('state').verbose_name
        self.assertEqual(state_label, 'state')

    def test_coord_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        coord_label = city_obj._meta.get_field('coord').verbose_name
        self.assertEqual(coord_label, 'coord')

    def test_weather_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        weather_label = city_obj._meta.get_field('weather').verbose_name
        self.assertEqual(weather_label, 'weather')

    def test_temp_code_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        temp_code_label = city_obj._meta.get_field('temp_code').verbose_name
        self.assertEqual(temp_code_label, 'temp code')

    def test_temperature_label(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        temperature_label = city_obj._meta.get_field('temperature').verbose_name
        self.assertEqual(temperature_label, 'temperature')

    def test_modify_city_id_null_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        city_obj.city_id = None
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_city_id_max_length_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_city_id_error = ''.join(
            random.choice(string.ascii_letters) for i in range(101)
        )

        city_obj.city_id = rand_city_id_error
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_city_id_valid_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_city_id_error = ''.join(
            random.choice(string.ascii_letters) for i in range(100)
        )

        city_obj.city_id = rand_city_id_error

        city_obj.save()

        self.assertEqual(city_obj.city_id, rand_city_id_error)

    def test_modify_name_null_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        city_obj.name = None
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_name_max_length_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_name_error = ''.join(
            random.choice(string.ascii_letters) for i in range(101)
        )

        city_obj.name = rand_name_error
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_name_valid_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_name_error = ''.join(
            random.choice(string.ascii_letters) for i in range(100)
        )

        city_obj.name = rand_name_error

        city_obj.save()

        self.assertEqual(city_obj.name, rand_name_error)

    def test_delete_country_city_deleted(self):
        country_list_obj = self.location_list[0]['country']
        city_list_obj = self.location_list[0]['city']

        country_obj = Country.objects.filter(name=country_list_obj.name).first()
        country_obj.delete()

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        self.assertEqual(city_obj, None)

    def test_modify_state_null_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        city_obj.state = None

        city_obj.save()

        self.assertEqual(city_obj.state, None)

    def test_modify_state_max_length_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_state_error = ''.join(
            random.choice(string.ascii_letters) for i in range(101)
        )

        city_obj.state = rand_state_error
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_state_valid_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_state_error = ''.join(
            random.choice(string.ascii_letters) for i in range(100)
        )

        city_obj.state = rand_state_error

        city_obj.save()

        self.assertEqual(city_obj.state, rand_state_error)

    def test_modify_state_null_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_state_error = ''.join(
            random.choice(string.ascii_letters) for i in range(100)
        )

        city_obj.coord = None
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_state_valid_json_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        new_json_dict = {'a': 'b'}

        city_obj.coord = new_json_dict

        city_obj.save()

        self.assertEqual(city_obj.coord, new_json_dict)

    def test_modify_temp_code_null_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        city_obj.temp_code = None

        city_obj.save()

        self.assertEqual(city_obj.temp_code, None)

    def test_modify_temp_code_max_length_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_temp_code_error = ''.join(
            random.choice(string.ascii_letters) for i in range(21)
        )

        city_obj.temp_code = rand_temp_code_error
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_temp_code_valid_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_temp_code_error = ''.join(
            random.choice(string.ascii_letters) for i in range(20)
        )

        city_obj.temp_code = rand_temp_code_error

        city_obj.save()

        self.assertEqual(city_obj.temp_code, rand_temp_code_error)

    def test_modify_temperature_null_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        city_obj.temperature = None

        city_obj.save()

        self.assertEqual(city_obj.temperature, None)

    def test_modify_temperature_max_length_fail(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_temperature_error = ''.join(
            random.choice(string.ascii_letters) for i in range(11)
        )

        city_obj.temperature = rand_temperature_error
        error_raised = False
        try:
            city_obj.save()
        except Exception as err:
            error_raised = True

        self.assertEqual(error_raised, True)

    def test_modify_temperature_valid_success(self):
        city_list_obj = self.location_list[0]['city']

        city_obj = City.objects.filter(city_id=city_list_obj.city_id).first()

        rand_temperature_error = ''.join(
            random.choice(string.ascii_letters) for i in range(10)
        )

        city_obj.temperature = rand_temperature_error

        city_obj.save()

        self.assertEqual(city_obj.temperature, rand_temperature_error)

    def test_return_string(self):
        city_list_obj = self.location_list[0]['city']

        self.assertEqual(str(city_list_obj), city_list_obj.name)
