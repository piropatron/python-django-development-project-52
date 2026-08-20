from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.forms import TaskCreateForm
from task_manager.tasks.models import Task


# Create your tests here.
class TasksTest(TestCase):
    fixtures = [
        'labels.json',
        "users.json",
        "statuses.json",
        "tasks.json"
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.login(username='dddddd', password='dddddd')

    def test_users_list(self):
        response = self.client.get(reverse("tasks.index"))
        self.assertEqual(response.status_code, 200)

    # ---------- IndexView ----------
    def test_index_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks.index'))
        self.assertRedirects(response, f'/login/?next={reverse("tasks.index")}')

    #
    def test_index_view_authenticated(self):
        response = self.client.get(reverse('tasks.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertIn('tasks_list', response.context)
        self.assertIn('filter', response.context)

    def test_index_view_pagination(self):
        response = self.client.get(reverse('tasks.index'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что на первой странице 10 объектов
        self.assertEqual(len(response.context['tasks_list']), 10)

        # Проверяем вторую страницу
        response = self.client.get(reverse('tasks.index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks_list']), 4)

    def test_index_view_filter(self):
        # Проверяем, что фильтр работает (только мои задачи)
        response = self.client.get(reverse('tasks.index') + '?only_my_task=on')
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks_list']
        # Ожидаем только задачи, где автор = текущий пользователь
        for task in tasks:
            self.assertEqual(task.author, self.user)

        task = Task.objects.get(id=4)
        # Проверяем, что задачи другого пользователя не отображаются
        self.assertNotIn(task, tasks)

    #
    # # ---------- CreateView ----------
    def test_create_view_get_authenticated(self):
        response = self.client.get(reverse('tasks.create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertIsInstance(response.context['form'], TaskCreateForm)

    def test_create_view_post_valid(self):
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': 1,
            'executor': 2,
            'labels': [1, 2],
            # другие поля, если есть
        }
        response = self.client.post(reverse('tasks.create'), data)
        self.assertRedirects(response, reverse('tasks.index'))
        # Проверяем, что задача создалась
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        task = Task.objects.get(name='New Task')
        self.assertEqual(task.author, self.user)

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('Task successfully created'))

    def test_create_view_post_invalid(self):
        data = {
            'name': '',  # обязательное поле, если есть
        }
        response = self.client.post(reverse('tasks.create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertFalse(Task.objects.filter(name='').exists())

    # ---------- UpdateView ----------
    def test_update_view_get_authenticated(self):
        response = self.client.get(reverse('tasks.update', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')
        self.assertEqual(response.context['task_id'], 1)
        self.assertIsInstance(response.context['form'], TaskCreateForm)
        task = Task.objects.get(id=1)
        self.assertEqual(response.context['form'].instance, task)

    def test_update_view_post_valid(self):
        data = {
            'name': 'Updated Title',
            'description': 'Updated Description',
            'status': 1,
            'executor': 2,
            'labels': [1, 2],
        }
        response = self.client.post(
            reverse('tasks.update', args=[1]), data
        )
        task = Task.objects.get(id=1)
        self.assertRedirects(response, reverse('tasks.index'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Title')
        self.assertEqual(task.description, 'Updated Description')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('Task successfully updated'))

    def test_update_view_post_invalid(self):
        data = {
            'name': '123',
        }
        task = Task.objects.get(id=1)
        response = self.client.post(
            reverse('tasks.update', args=[1]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')
        task.refresh_from_db()
        self.assertNotEqual(task.name, '123')

    #
    # # ---------- DeleteView ----------
    def test_delete_view_get_authenticated(self):
        response = self.client.get(reverse('tasks.delete', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')
        self.assertEqual(response.context['task_id'], 1)

    def test_delete_view_post(self):
        response = self.client.post(reverse('tasks.delete', args=[1]))
        self.assertRedirects(response, reverse('tasks.index'))
        self.assertFalse(Task.objects.filter(id=1).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('Task successfully deleted'))

    def test_delete_view_post_nonexistent(self):
        # Проверяем, что при попытке удалить несуществующую задачу возвращается 404
        response = self.client.post(reverse('tasks.delete', args=[99999]))
        self.assertEqual(response.status_code, 404)

    # # ---------- DetailView ----------
    def test_detail_view_authenticated(self):
        task = Task.objects.get(id=1)
        response = self.client.get(reverse('tasks.detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')
        self.assertEqual(response.context['task'], task)

    #
    def test_detail_view_nonexistent(self):
        response = self.client.get(reverse('tasks.detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    # ---------- Permissions (not required by code but we can test) ----------
    def test_create_view_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('tasks.create'))
        self.assertEqual(response.status_code, 200)  # доступ открыт

    def test_update_view_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('tasks.update', args=[1]))
        self.assertEqual(response.status_code, 200)

    #
    def test_delete_view_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('tasks.delete', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('tasks.detail', args=[1]))
        self.assertEqual(response.status_code, 200)
