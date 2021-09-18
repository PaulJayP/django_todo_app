from django.test import Client
from django.urls import reverse

from todo_list.forms import TodoFormUpdate
from todo_list.models import TodoItem
from todo_list.tests.api.todo_list_case_mixin import TodoListViewsMixin


class ViewEditFormTestCase(TodoListViewsMixin):

    def setUp(self):
        super().setUp()

    # Not logged in, unauthorised
    def test_get_edit_form_with_valid_id_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        response = client.post(
            reverse('edit_form',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/edit_form/{0}'.format(todo_item_obj['id']),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_get_edit_form_with_invalid_id_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        invalid_id = 1000

        response = client.post(
            reverse('edit_form',
                    kwargs={
                        'task_id': invalid_id
                    }),
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/edit_form/{0}'.format(invalid_id),
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, authorised
    def test_get_edit_form_with_valid_id_authorised_success(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        client.force_login(self.test_user_1)

        response = client.post(
            reverse('edit_form',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['forms'], TodoFormUpdate)
        self.assertEqual(response.context['task_id'], todo_item_obj['id'])
        self.assertTemplateUsed(response, 'edit.html')

    def test_get_edit_form_with_invalid_id_authorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        client.force_login(self.test_user_1)

        invalid_id = 1000

        response = client.post(
            reverse('edit_form',
                    kwargs={
                        'task_id': invalid_id
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not found')
        self.assertRedirects(
            response, '/index/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, unauthorised
    def test_get_edit_form_with_valid_id_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        client.force_login(self.test_user_2)

        response = client.post(
            reverse('edit_form',
                    kwargs={
                        'task_id': todo_item_obj['id']
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Unauthorized to view this page')
        self.assertRedirects(
            response, '/index/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    def test_get_edit_form_with_invalid_id_unauthorised_fail(self):

        todo_item_obj = TodoItem.objects.filter(user=self.users[0]).values().first()

        client = Client()

        client.force_login(self.test_user_1)

        invalid_id = 1000

        response = client.post(
            reverse('edit_form',
                    kwargs={
                        'task_id': invalid_id
                    }),
        )

        resp_messages = list(m.message for m in response.wsgi_request._messages)
        self.assertEqual(resp_messages[0], 'Task not found')
        self.assertRedirects(
            response, '/index/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
