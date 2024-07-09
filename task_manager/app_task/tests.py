from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.app_task.models import Task
from task_manager.app_status.models import Status
from task_manager.app_tag.models import Tag


class TaskTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')

        self.status = Status.objects.create(
            name='Open',
            description='Task is open'
        )
        self.tag = Tag.objects.create(
            name='Urgent',
            description='Urgent task'
        )

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status=self.status,
            assignee=self.user,
            author=self.user
        )
        self.task.tags.add(self.tag)

    def test_create_task_view(self):
        url = reverse('task_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_create_task(self):
        url = reverse('task_create')
        task_data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'assignee': self.user.id,
            'tags': [self.tag.id]
        }
        response = self.client.post(url, task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_update_task_view(self):
        url = reverse('task_update', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

    def test_update_task(self):
        url = reverse('task_update', args=[self.task.pk])
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'assignee': self.user.id,
            'tags': [self.tag.id]
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')

    def test_delete_task_view(self):
        url = reverse('task_delete', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_delete_task(self):
        url = reverse('task_delete', args=[self.task.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(title='Test Task').exists())

    def test_task_list_view(self):
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        url = reverse('task_view', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')
        self.assertContains(response, 'Test Task')
