from datetime import datetime

from django.test import Client
from django.urls import reverse
from django.utils.timezone import get_current_timezone

from todo_list.models import TodoItem
from todo_list.tests.api.todo_list_case_mixin import TodoListViewsMixin


class ViewEditTaskTestCase(TodoListViewsMixin):

    def setUp(self):
        super().setUp()

    # Not logged in, unauthorised
    def test_post_edit_task_with_valid_id_with_body_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        client = Client()

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
            data=todo_item_obj
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/edit_task/{0}'.format(todo_item_obj['id']),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_post_edit_task_with_invalid_id_with_body_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        invalid_id = 1000

        client = Client()

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': invalid_id
                    }),
            data=todo_item_obj
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/edit_task/{0}'.format(invalid_id),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_post_edit_task_with_valid_id_no_body_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        client = Client()

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/edit_task/{0}'.format(todo_item_obj['id']),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in and authorised
    def test_post_edit_task_with_valid_id_with_body_authorised_success(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
            data=todo_item_obj
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_messages[0], 'Task updated')

    def test_post_edit_task_with_invalid_id_with_body_authorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        invalid_id = 1000

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': invalid_id
                    }),
            data=todo_item_obj
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertRedirects(
            response, '/index/', status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(resp_messages[0], 'Task not found')

    def test_post_edit_task_with_valid_id_no_body_authorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not updated')
        self.assertRedirects(
            response, '/edit_form/{0}'.format(todo_item_obj['id']), status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, unauthorised
    def test_post_edit_task_with_valid_id_with_body_logged_in_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        client = Client()
        # Unauthorized login
        client.force_login(self.test_user_2)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
            data=todo_item_obj
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertRedirects(
            response, '/index/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(resp_messages[0], 'Unauthorized to edit this task')

    def test_post_edit_task_with_invalid_id_with_body_logged_in_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        invalid_id = 1000

        client = Client()
        # Unauthorized login
        client.force_login(self.test_user_2)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': invalid_id
                    }),
            data=todo_item_obj
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertRedirects(
            response, '/index/', status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(resp_messages[0], 'Task not found')

    def test_post_edit_task_with_valid_id_no_body_logged_in_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        client = Client()
        # Unauthorized login
        client.force_login(self.test_user_2)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertRedirects(
            response, '/index/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertEqual(resp_messages[0], 'Unauthorized to edit this task')

    # Logged in, authorised, missing fields validation
    def test_post_edit_task_with_id_missing_location_authorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
            data=todo_item_obj
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not updated')
        self.assertRedirects(
            response, '/edit_form/{0}'.format(todo_item_obj['id']), status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_post_edit_task_with_id_missing_title_authorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        todo_item_obj['completed_at'] = datetime.now(tz=get_current_timezone())

        todo_item_obj['country'] = [todo_item_obj['country_id']]
        todo_item_obj['city'] = [todo_item_obj['city_id']]

        todo_item_obj.pop('title')

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('edit_task',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
            data=todo_item_obj
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not updated')
        self.assertRedirects(
            response, '/edit_form/{0}'.format(todo_item_obj['id']), status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )