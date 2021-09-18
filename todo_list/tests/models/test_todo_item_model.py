import random
import string
import uuid
from datetime import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import make_aware, get_current_timezone

from location.models.city_model import City
from location.models.country_model import Country
from todo_list.models import TodoItem


class TodoItemTestCase(TestCase):

    def setUp(self):
        test_time = datetime.now(tz=get_current_timezone())
        with mock.patch('django.utils.timezone.now') as mock_auto_date:
            mock_auto_date.return_value = test_time

            self.test_user = User.objects.create_user(username='test_user', password='test_pass')
            self.test_user.save()

            self.task_item = TodoItem.objects.create(
                title="A test title",
                content="A little bit of test content",
                user=self.test_user
            )
            self.task_item.save()

            self.test_country = Country.objects.create(name="test_country")
            self.test_country.save()

            self.test_city = City.objects.create(
                country=self.test_country,
                city_id=str(uuid.uuid4()),
                coord={"lon": 01.111111, "lat": 01.111111}
            )
            self.test_city.save()

    def test_title_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        title_label = task_item._meta.get_field('title').verbose_name
        self.assertEqual(title_label, 'title')

    def test_title_max_length(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        max_length = task_item._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_content_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        content_label = task_item._meta.get_field('content').verbose_name
        self.assertEqual(content_label, 'content')

    def test_updated_at_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        updated_at_label = task_item._meta.get_field('updated_at').verbose_name
        self.assertEqual(updated_at_label, 'updated at')

    def test_created_at_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        created_at_label = task_item._meta.get_field('created_at').verbose_name
        self.assertEqual(created_at_label, 'created at')

    def test_completed_at_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        completed_at_label = task_item._meta.get_field('completed_at').verbose_name
        self.assertEqual(completed_at_label, 'completed at')

    def test_user_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        user_label = task_item._meta.get_field('user').verbose_name
        self.assertEqual(user_label, 'user')

    def test_country_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        country__label = task_item._meta.get_field('country').verbose_name
        self.assertEqual(country__label, 'country')

    def test_city_label(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        city_label = task_item._meta.get_field('city').verbose_name
        self.assertEqual(city_label, 'city')

    def test_return_string(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        expected_object_name = 'TodoItem(title={0}, content={1}, created_at={2}, updated_at={3}, completed_at={4})'.format(
            task_item.title,
            task_item.content,
            task_item.created_at,
            task_item.updated_at,
            task_item.completed_at,
        )
        self.assertEqual(str(task_item), expected_object_name)

    def test_created_at_is_datetime(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        self.assertIsInstance(task_item.created_at, datetime)

    def test_updated_at_is_datetime(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        self.assertIsInstance(task_item.updated_at, datetime)

    def test_modify_updated_at(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()

        previous_datetime = task_item.updated_at

        task_item.save()

        new_datetime = task_item.updated_at

        self.assertGreaterEqual(new_datetime, previous_datetime)

    def test_modify_completed_at(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        self.assertEqual(task_item.completed_at, None)

        new_datetime = make_aware(datetime.utcnow())
        task_item.completed_at = new_datetime
        task_item.save()

        self.assertEqual(task_item.completed_at, new_datetime)

    def test_modify_title(self):

        rand_title_max = ''.join(random.choice(string.ascii_letters) for i in range(100))
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        task_item.title = rand_title_max
        task_item.save()

        self.assertEqual(task_item.title, rand_title_max)

        rand_title_error = ''.join(random.choice(string.ascii_letters) for i in range(101))
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        task_item.title = rand_title_error

        error_raised = False
        try:
            task_item.save()
        except Exception as err:
            error_raised = True
        self.assertEqual(error_raised, True)

    def test_modify_content(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        old_content = task_item.content

        rand_content = ''.join(random.choice(string.ascii_letters) for i in range(50))
        task_item.content = rand_content
        task_item.save()

        self.assertEqual(task_item.content, rand_content)

    def test_add_country(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        self.assertEqual(task_item.country, None)

        country_item = Country.objects.filter(name=self.test_country.name).first()
        task_item.country = country_item
        task_item.save()

        self.assertEqual(task_item.country, country_item)

    def test_add_city(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        self.assertEqual(task_item.city, None)

        city_item = City.objects.filter(country=self.test_city.country).first()
        task_item.city = city_item
        task_item.save()

        self.assertEqual(task_item.city, city_item)

    def test_delete_country_and_city(self):
        task_item = TodoItem.objects.filter(user=self.test_user).first()
        self.assertEqual(task_item.city, None)

        country_item = Country.objects.filter(name=self.test_country.name).first()
        city_item = City.objects.filter(country=self.test_country).first()

        task_item.city = city_item
        task_item.country = country_item
        task_item.save()

        self.assertEqual(task_item.city, city_item)
        self.assertEqual(task_item.country, country_item)

        city_item.delete()
        country_item.delete()

        task_item = TodoItem.objects.filter(user=self.test_user).first()

        self.assertEqual(task_item.city, None)
        self.assertEqual(task_item.country, None)

    def test_delete_user_cascade_task(self):

        user_item = User.objects.filter(username=self.test_user.username).first()
        user_item.delete()

        task_item = TodoItem.objects.filter(user=self.test_user).first()

        self.assertEqual(task_item, None)

