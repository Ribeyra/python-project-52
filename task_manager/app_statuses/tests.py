from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status


class StatusTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword123'
        )
        self.client.login(
            username='testuser', password='testpassword123'
        )
        self.status = Status.objects.create(
            name='Test Status', description='Test Description'
        )

    def test_create_status_view(self):
        url = reverse('status_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

    def test_create_status(self):
        url = reverse('status_create')
        status_data = {
            'name': 'New Status',
            'description': 'New Description'
        }
        response = self.client.post(url, status_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_update_status_view(self):
        url = reverse('status_update', args=[self.status.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_update_status(self):
        url = reverse('status_update', args=[self.status.pk])
        updated_data = {
            'name': 'Updated Status',
            'description': 'Updated Description'
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')
        self.assertEqual(self.status.description, 'Updated Description')

    def test_delete_status_view(self):
        url = reverse('status_delete', args=[self.status.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_delete_status(self):
        url = reverse('status_delete', args=[self.status.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(name='Test Status').exists())

    def test_status_list_view(self):
        url = reverse('statuses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertContains(response, 'Test Status')
