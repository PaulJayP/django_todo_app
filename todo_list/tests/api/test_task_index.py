
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from location.models.city_model import City
from location.models.country_model import Country
from todo_list.forms import TodoForm
from todo_list.models import TodoItem
from todo_list.tests.api.todo_list_case_mixin import TodoListViewsMixin


class ViewIndexListViewTestCase(TodoListViewsMixin):

    def setUp(self):
        super().setUp()

    def test_ensure_correct_number_of_test_data(self):
        users = User.objects.all()
        tasks = TodoItem.objects.all()
        cities = City.objects.all()
        countries = Country.objects.all()

        self.assertEqual(users.count(), 2)
        self.assertEqual(tasks.count(), 6)
        self.assertEqual(cities.count(), 6)
        self.assertEqual(countries.count(), 6)

    def test_get_index_success_anonymous_user(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_get_index_success_has_template_anonymous_user(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_get_index_success_has_title_anonymous_user(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.context['title'], "TODO LIST")

    def test_get_index_success_has_list_anonymous_user(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(len(response.context['list']), 6)

    def test_get_index_success_has_form_anonymous_user(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertIsInstance(response.context['forms'], TodoForm)

    def test_get_index_success_as_user_1(self):
        client = Client()
        client.force_login(self.test_user_1)
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_get_index_success_has_template_as_user_1(self):
        client = Client()
        client.force_login(self.test_user_1)
        response = client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_get_index_success_has_title_as_user_1(self):
        client = Client()
        client.force_login(self.test_user_1)
        response = client.get(reverse('index'))
        self.assertEqual(response.context['title'], "TODO LIST")

    def test_get_index_success_has_list_as_user_1(self):
        client = Client()
        client.force_login(self.test_user_1)
        response = client.get(reverse('index'))
        self.assertEqual(len(response.context['list']), 3)

        for task in response.context['list']:
            self.assertIn('test_user_1', task.content)

    def test_get_index_success_has_form_as_user_1(self):
        client = Client()
        client.force_login(self.test_user_1)
        response = client.get(reverse('index'))
        self.assertIsInstance(response.context['forms'], TodoForm)

    def test_get_index_success_as_user_2(self):
        client = Client()
        client.force_login(self.test_user_2)
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_get_index_success_has_template_as_user_2(self):
        client = Client()
        client.force_login(self.test_user_2)
        response = client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_get_index_success_has_title_as_user_2(self):
        client = Client()
        client.force_login(self.test_user_2)
        response = client.get(reverse('index'))
        self.assertEqual(response.context['title'], "TODO LIST")

    def test_get_index_success_has_list_as_user_2(self):
        client = Client()
        client.force_login(self.test_user_2)
        response = client.get(reverse('index'))
        self.assertEqual(len(response.context['list']), 3)

        for task in response.context['list']:
            self.assertIn('test_user_2', task.content)

    def test_get_index_success_has_form_as_user_2(self):
        client = Client()
        client.force_login(self.test_user_2)
        response = client.get(reverse('index'))
        self.assertIsInstance(response.context['forms'], TodoForm)
