from django.test import Client
from django.urls import reverse

from todo_list.models import TodoItem
from todo_list.tests.api.todo_list_case_mixin import TodoListViewsMixin


class ViewCreateTaskTestCase(TodoListViewsMixin):

    def setUp(self):
        super().setUp()

    def get_task_item(self):
        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        return {
            'title': ['new_test_tile'],
            'content': ['new_test_content'],
            'country': [todo_item_obj['country_id']],
            'city': [todo_item_obj['city_id']]
        }

    # Not logged in, unauthorised
    def test_post_create_task_with_body_unauthorised_fail(self):

        client = Client()

        response = client.post(
            reverse('create'), data=self.get_task_item()
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/create/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, authorised
    def test_post_create_task_with_body_authorised_success(self):

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('create'), data=self.get_task_item()
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task created')
        self.assertEqual(response.status_code, 200)

    def test_post_create_task_with_invalid_location_authorised_fail(self):
        client = Client()
        client.force_login(self.test_user_1)

        post_data = self.get_task_item()

        post_data['country'] = ['0']
        post_data['city'] = ['0']

        response = client.post(
            reverse('create'), data=post_data
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not created')
        self.assertRedirects(
            response, '/create_form/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_post_create_task_with_null_title_authorised_fail(self):
        client = Client()
        client.force_login(self.test_user_1)

        post_data = self.get_task_item()

        post_data.pop('title')

        response = client.post(
            reverse('create'), data=post_data
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not created')
        self.assertRedirects(
            response, '/create_form/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
