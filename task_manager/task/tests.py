from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.task.models import Task
from task_manager.status.models import Status
from task_manager.label.models import Label


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
        self.labels = Label.objects.create(
            name='Urgent',
            description='Urgent task'
        )

        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            executor=self.user,
            author=self.user
        )
        self.task.labels.add(self.labels)

    def test_create_task_view(self):
        url = reverse('task_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_create_task(self):
        url = reverse('task_create')
        task_data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.labels.id]
        }
        response = self.client.post(url, task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_update_task_view(self):
        url = reverse('task_update', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

    def test_update_task(self):
        url = reverse('task_update', args=[self.task.pk])
        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.labels.id]
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
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
        self.assertFalse(Task.objects.filter(name='Test Task').exists())

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


class TaskFilterTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            password='password123'
        )
        self.client.login(username='user1', password='password123')

        self.status1 = Status.objects.create(
            name='Open',
            description='Open tasks'
        )
        self.status2 = Status.objects.create(
            name='Closed',
            description='Closed tasks'
        )

        self.labels1 = Label.objects.create(
            name='Bug',
            description='Bug related task'
        )
        self.labels2 = Label.objects.create(
            name='Feature',
            description='Feature related task'
        )

        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status1,
            executor=self.user1,
            author=self.user1
        )
        self.task1.labels.add(self.labels1)

        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            status=self.status2,
            executor=self.user2,
            author=self.user2
        )
        self.task2.labels.add(self.labels2)

    def test_filter_by_status(self):
        url = reverse('tasks')
        response = self.client.get(url, {'status': self.status1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_executor(self):
        url = reverse('tasks')
        response = self.client.get(url, {'executor': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_labels(self):
        url = reverse('tasks')
        response = self.client.get(url, {'labels': self.labels1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_self_tasks(self):
        url = reverse('tasks')
        response = self.client.get(url, {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_combined(self):
        url = reverse('tasks')
        response = self.client.get(url, {
            'status': self.status1.id,
            'executor': self.user1.id,
            'labels': self.labels1.id,
            'self_tasks': 'on'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
