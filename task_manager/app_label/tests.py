from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Label


class LabelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
        self.label = Label.objects.create(
            name='Test Label',
            description='Test Description'
        )

    def test_create_label_view(self):
        url = reverse('label_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

    def test_create_label(self):
        url = reverse('label_create')
        label_data = {
            'name': 'New Label',
            'description': 'New Description'
        }
        response = self.client.post(url, label_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_update_label_view(self):
        url = reverse('label_update', args=[self.label.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

    def test_update_label(self):
        url = reverse('label_update', args=[self.label.pk])
        updated_data = {
            'name': 'Updated Label',
            'description': 'Updated Description'
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')
        self.assertEqual(self.label.description, 'Updated Description')

    def test_delete_label_view(self):
        url = reverse('label_delete', args=[self.label.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

    def test_delete_label(self):
        url = reverse('label_delete', args=[self.label.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(name='Test Label').exists())

    def test_label_list_view(self):
        url = reverse('labels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')
        self.assertContains(response, 'Test Label')
