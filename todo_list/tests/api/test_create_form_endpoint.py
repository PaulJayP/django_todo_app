from django.test import Client
from django.urls import reverse

from todo_list.forms import TodoForm
from todo_list.tests.api.todo_list_case_mixin import TodoListViewsMixin


class ViewCreateFormTestCase(TodoListViewsMixin):

    def setUp(self):
        super().setUp()

    # Not logged in, unauthorised
    def test_get_create_form_unauthorised_fail(self):

        client = Client()

        response = client.get(
            reverse('create_form')
        )

        self.assertRedirects(
            response, '/accounts/login/?next=/create_form/',
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )

    # Logged in, authorised
    def test_get_create_form_authorised_success(self):

        client = Client()
        client.force_login(self.test_user_1)

        response = client.get(
            reverse('create_form')
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['forms'], TodoForm)
