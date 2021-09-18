from todo_list.models import TodoItem
from todo_list.tests.api.todo_list_case_mixin import TodoListViewsMixin
from django.test import Client
from django.urls import reverse


class ViewDeleteTaskTestCase(TodoListViewsMixin):

    def setUp(self):
        super().setUp()

    # Not logged in, unauthorised
    def test_delete_valid_task_unauthorised_fail(self):
        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        response = client.post(
            reverse('delete',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/delete/{0}'.format(todo_item_obj['id']),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_delete_invalid_task_unauthorised_fail(self):
        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        invalid_id = 10000

        response = client.post(
            reverse('delete',
                    kwargs={
                        'task_id': invalid_id
                    }),
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/delete/{0}'.format(invalid_id),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, authorised
    def test_delete_valid_task_authorised_success(self):
        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()
        client.force_login(self.test_user_1)

        response = client.post(
            reverse('delete',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task removed')
        self.assertEqual(response.status_code, 200)

    def test_delete_invalid_task_authorised_fail(self):
        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()
        client.force_login(self.test_user_1)

        invalid_id = 10000

        response = client.post(
            reverse('delete',
                    kwargs={
                        'task_id': invalid_id
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not found')
        self.assertRedirects(
            response, '/index/'.format(invalid_id),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, unauthorised
    def test_delete_valid_task_logged_in_unauthorised_fail(self):
        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()
        client.force_login(self.test_user_2)

        response = client.post(
            reverse('delete',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Unauthorized to delete this task')
        self.assertRedirects(
            response, '/index/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
