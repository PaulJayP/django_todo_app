from datetime import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import make_aware

from todo_list.models import TodoItem


class TodoItemTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ Set up base test data"""

        test_time = datetime.now()
        with mock.patch('django.utils.timezone.now') as mock_auto_date:
            mock_auto_date.return_value = test_time

            cls.test_user = User.objects.create_user(username='test_user', password='test_pass')
            cls.task_item = TodoItem.objects.create(
                title="A test title",
                content="A little bit of test content",
                user=cls.test_user
            )

    def test_title_label(self):
        task_item = TodoItem.objects.get(id=1)
        title_label = task_item._meta.get_field('title').verbose_name
        self.assertEqual(title_label, 'title')

    def test_title_max_length(self):
        task_item = TodoItem.objects.get(id=1)
        max_length = task_item._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_content_label(self):
        task_item = TodoItem.objects.get(id=1)
        content_label = task_item._meta.get_field('content').verbose_name
        self.assertEqual(content_label, 'content')

    def test_updated_at_label(self):
        task_item = TodoItem.objects.get(id=1)
        updated_at_label = task_item._meta.get_field('updated_at').verbose_name
        self.assertEqual(updated_at_label, 'updated_at')

    def test_created_at_label(self):
        task_item = TodoItem.objects.get(id=1)
        created_at_label = task_item._meta.get_field('created_at').verbose_name
        self.assertEqual(created_at_label, 'created_at')

    def test_completed_at_label(self):
        task_item = TodoItem.objects.get(id=1)
        completed_at_label = task_item._meta.get_field('completed_at').verbose_name
        self.assertEqual(completed_at_label, 'completed_at')

    def test_user_label(self):
        task_item = TodoItem.objects.get(id=1)
        user_label = task_item._meta.get_field('user').verbose_name
        self.assertEqual(user_label, 'user')

    def test_country_label(self):
        task_item = TodoItem.objects.get(id=1)
        country__label = task_item._meta.get_field('country').verbose_name
        self.assertEqual(country__label, 'country')

    def test_city_label(self):
        task_item = TodoItem.objects.get(id=1)
        city_label = task_item._meta.get_field('city').verbose_name
        self.assertEqual(city_label, 'city')

    def test_return_string(self):
        task_item = TodoItem.objects.get(id=1)
        expected_object_name = 'TodoItem(title={0}, content={1}, created_at={2}, updated_at={3}, completed_at={4})'.format(
            task_item.title,
            task_item.content,
            task_item.created_at,
            task_item.updated_at,
            task_item.completed_at,
        )
        self.assertEqual(str(task_item), expected_object_name)

    def test_modify_completed_at(self):
        task_item = TodoItem.objects.get(id=1)
        self.assertEqual(task_item.completed_at, None)
        task_item.completed_at = make_aware(datetime.utcnow())
        pass

    def test_add_country(self):
        pass

    def test_add_city(self):
        pass

    def test_delete_user_cascade_task(self):
        pass
