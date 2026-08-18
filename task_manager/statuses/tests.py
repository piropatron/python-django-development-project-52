from django.contrib.auth.models import User

# Create your tests here.
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import Status


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        # Create some statuses
        self.status1 = Status.objects.create(name='Status 1')
        self.status2 = Status.objects.create(name='Status 2')

    def test_index_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('statuses.index'))
        self.assertRedirects(response, '/login/?next=' + reverse('statuses.index'))

    def test_index_view_logged_in_returns_200_and_uses_correct_template(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('statuses.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_index_view_context_contains_statuses(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('statuses.index'))
        self.assertIn('statuses', response.context)
        statuses = response.context['statuses']
        self.assertGreaterEqual(statuses.count(), 2)
        self.assertLessEqual(statuses.count(), 15)
        self.assertIn(self.status1, statuses)
        self.assertIn(self.status2, statuses)


class CreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_create_view_get_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('statuses.create'))
        self.assertRedirects(response, '/login/?next=' + reverse('statuses.create'))

    def test_create_view_get_logged_in_returns_200_and_uses_correct_template(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('statuses.create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertIn('form', response.context)

    def test_create_view_post_valid_data_creates_status_and_redirects(self):
        self.client.login(username='testuser', password='pass')
        valid_data = {'name': 'New Status'}
        response = self.client.post(reverse('statuses.create'), data=valid_data)
        self.assertRedirects(response, reverse('statuses.index'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_create_view_post_invalid_data_renders_form_with_errors(self):
        self.client.login(username='testuser', password='pass')
        invalid_data = {'name': ''}  # assuming name is required
        response = self.client.post(reverse('statuses.create'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertFalse(Status.objects.filter(name='').exists())


class UpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.status = Status.objects.create(name='Old Status')

    def test_update_view_get_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('statuses.update', kwargs={'pk': self.status.pk}))
        self.assertRedirects(response, '/login/?next=' + reverse('statuses.update', kwargs={'pk': self.status.pk}))

    def test_update_view_get_logged_in_returns_200_and_uses_correct_template(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('statuses.update', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['status_id'], self.status.pk)
        # Check that form is bound with instance
        form = response.context['form']
        self.assertEqual(form.instance.pk, self.status.pk)

    def test_update_view_post_valid_data_updates_status_and_redirects(self):
        self.client.login(username='testuser', password='pass')
        valid_data = {'name': 'Updated Status'}
        response = self.client.post(reverse('statuses.update', kwargs={'pk': self.status.pk}), data=valid_data)
        self.assertRedirects(response, reverse('statuses.index'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

    def test_update_view_post_invalid_data_renders_form_with_errors(self):
        self.client.login(username='testuser', password='pass')
        invalid_data = {'name': ''}
        response = self.client.post(reverse('statuses.update', kwargs={'pk': self.status.pk}), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        # Ensure status not changed
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Old Status')


class DeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.status = Status.objects.create(name='Status to delete')

    def test_delete_view_get_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('statuses.delete', kwargs={'pk': self.status.pk}))
        self.assertRedirects(response, '/login/?next=' + reverse('statuses.delete', kwargs={'pk': self.status.pk}))

    def test_delete_view_get_logged_in_returns_200_and_uses_correct_template(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('statuses.delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')
        self.assertEqual(response.context['status_id'], self.status.pk)

    def test_delete_view_post_deletes_status_and_redirects(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('statuses.delete', kwargs={'pk': self.status.pk}))
        self.assertRedirects(response, reverse('statuses.index'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

    def test_delete_view_post_handles_nonexistent_status_returns_404(self):
        # The view uses get_object_or_404, so it should raise 404 if not found
        self.client.login(username='testuser', password='pass')
        non_existent_pk = self.status.pk + 100
        response = self.client.post(reverse('statuses.delete', kwargs={'pk': non_existent_pk}))
        self.assertEqual(response.status_code, 404)