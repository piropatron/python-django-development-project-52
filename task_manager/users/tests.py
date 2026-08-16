from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class IndexViewTest(TestCase):
    def test_index_view_returns_200_and_uses_correct_template(self):
        response = self.client.get(reverse('users.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_index_view_context_contains_users(self):
        # Create some users
        User.objects.create_user(username='user1', password='pass')
        User.objects.create_user(username='user2', password='pass')
        response = self.client.get(reverse('users.index'))
        self.assertIn('users', response.context)
        users = response.context['users']
        # Should contain at most 15 users, and include created ones
        self.assertGreaterEqual(users.count(), 2)
        self.assertLessEqual(users.count(), 15)


class CreateViewTest(TestCase):
    def test_create_view_get_returns_200_and_uses_correct_template(self):
        response = self.client.get(reverse('users.create'))  # assuming name 'users.create'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_create_view_post_valid_data_creates_user_and_redirects(self):
        valid_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('users.create'), data=valid_data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The user has been successfully registered.')

    def test_create_view_post_invalid_data_renders_form_with_errors(self):
        invalid_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'wrongpass',
        }
        response = self.client.post(reverse('users.create'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertFalse(User.objects.filter(username='testuser').exists())


class UpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')

    def test_update_view_get_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('users.update', kwargs={'pk': self.user.pk}))
        # Redirects to login (default login url is /login/)
        self.assertRedirects(response, '/login/?next=' + reverse('users.update', kwargs={'pk': self.user.pk}))

    def test_update_view_get_for_other_user_redirects_with_message(self):
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(reverse('users.update', kwargs={'pk': self.user.pk}))
        self.assertRedirects(response, reverse('users.index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have permission to make changes.')

    def test_update_view_get_for_own_user_returns_200_and_uses_correct_template(self):
        self.client.login(username='testuser', password='oldpass')
        response = self.client.get(reverse('users.update', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['user_id'], self.user.pk)

    def test_update_view_post_valid_data_updates_user_and_redirects(self):
        self.client.login(username='testuser', password='oldpass')
        valid_data = {
            'username': 'testuser',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.post(reverse('users.update', kwargs={'pk': self.user.pk}), data=valid_data)
        self.assertRedirects(response, reverse('users.index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User successfully modified')

    def test_update_view_post_invalid_data_renders_form_with_errors(self):
        self.client.login(username='testuser', password='oldpass')
        invalid_data = {
            'username': '',  # empty username is invalid
            'first_name': 'Updated',
        }
        response = self.client.post(reverse('users.update', kwargs={'pk': self.user.pk}), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)


class DeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')

    def test_delete_view_get_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('users.delete', kwargs={'pk': self.user.pk}))
        self.assertRedirects(response, '/login/?next=' + reverse('users.delete', kwargs={'pk': self.user.pk}))

    def test_delete_view_get_logged_in_returns_200_and_uses_correct_template(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('users.delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertEqual(response.context['user_id'], self.user.pk)

    def test_delete_view_post_deletes_user_and_redirects(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('users.delete', kwargs={'pk': self.user.pk}))
        self.assertRedirects(response, reverse('users.index'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User successfully deleted')

    def test_delete_view_post_can_delete_other_user(self):
        # The view allows deletion of any user when logged in (no ownership check)
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('users.delete', kwargs={'pk': self.other_user.pk}))
        self.assertRedirects(response, reverse('users.index'))
        self.assertFalse(User.objects.filter(pk=self.other_user.pk).exists())