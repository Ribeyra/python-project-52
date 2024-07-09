from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Tag


class TagTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
        self.tag = Tag.objects.create(
            name='Test Tag',
            description='Test Description'
        )

    def test_create_tag_view(self):
        url = reverse('tag_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tags/create.html')

    def test_create_tag(self):
        url = reverse('tag_create')
        tag_data = {
            'name': 'New Tag',
            'description': 'New Description'
        }
        response = self.client.post(url, tag_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tags'))
        self.assertTrue(Tag.objects.filter(name='New Tag').exists())

    def test_update_tag_view(self):
        url = reverse('tag_update', args=[self.tag.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tags/update.html')

    def test_update_tag(self):
        url = reverse('tag_update', args=[self.tag.pk])
        updated_data = {
            'name': 'Updated Tag',
            'description': 'Updated Description'
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tags'))
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Updated Tag')
        self.assertEqual(self.tag.description, 'Updated Description')

    def test_delete_tag_view(self):
        url = reverse('tag_delete', args=[self.tag.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tags/delete.html')

    def test_delete_tag(self):
        url = reverse('tag_delete', args=[self.tag.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tags'))
        self.assertFalse(Tag.objects.filter(name='Test Tag').exists())

    def test_tag_list_view(self):
        url = reverse('tags')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tags/index.html')
        self.assertContains(response, 'Test Tag')
