import uuid
from datetime import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.test.testcases import SerializeMixin
from django.utils.timezone import get_current_timezone
from django.test import TestCase

from location.models.city_model import City
from location.models.country_model import Country
from todo_list.models import TodoItem


class TodoListViewsMixin(SerializeMixin, TestCase):

    lockfile = __file__

    def setUp(self):
        # Create users
        self.users = self.create_users()

        # Create tasks per user
        self.users_task_list = self.create_tasks(user_list=self.users)

    def create_users(self) -> list[User]:
        self.test_user_1 = User.objects.create_user(username='test_user_1', password='test_pass_1')
        self.test_user_2 = User.objects.create_user(username='test_user_2', password='test_pass_2')

        return [self.test_user_1, self.test_user_2]

    def create_tasks(self, user_list: list[User]):

        users_tasks_list = []

        with mock.patch('django.utils.timezone.now') as mock_auto_date:
            for user_obj in user_list:

                task_list = []
                user_task_dict = {}

                test_time = datetime.now(tz=get_current_timezone())
                mock_auto_date.return_value = test_time

                for index in range(3):

                    test_country = Country.objects.create(name="test_country [{0}]".format(str(uuid.uuid4())[:25]))
                    test_city = City.objects.create(
                        country=test_country,
                        city_id=str(uuid.uuid4()),
                        coord={"lon": 01.111111, "lat": 01.111111}
                    )

                    self.task_item = TodoItem.objects.create(
                        title="A test title - User: [{0}] | Index: [{1}]".format(user_obj.username, index),
                        content="A little bit of test content - User: [{0}] | Index: [{1}]".format(
                            user_obj.username, index
                        ),
                        user=user_obj,
                        city=test_city,
                        country=test_country

                    )

                    task_list.append(self.task_item)

                user_task_dict['user'] = user_obj
                user_task_dict['tasks'] = task_list
                users_tasks_list.append(user_task_dict)

        return users_tasks_list
