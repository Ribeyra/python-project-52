from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class CreateUserTest(TestCase):
    def test_create_user_view(self):
        url = reverse('user_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_create_user(self):
        url = reverse('user_create')
        user_data = {
            'username': 'testuser',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, user_data)
        if response.status_code != 302:
            print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(get_user_model().objects.filter(
            username='testuser'
        ).exists())


class UpdateUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(username='testuser', password='Testpassword123')

    def test_update_user_view(self):
        url = reverse('user_update', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_update_user(self):
        url = reverse('user_update', args=[self.user.pk])
        updated_data = {
            'username': 'updateduser',
            'password1': 'Newpassword123',
            'password2': 'Newpassword123',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.post(url, updated_data)
        if response.status_code != 302:
            print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')


class DeleteUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpassword123'
        )
        self.client.login(username='testuser', password='Testpassword123')

    def test_delete_user_view(self):
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_delete_user(self):
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(get_user_model().objects.filter(
            username='testuser'
        ).exists())


class UserListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpassword123'
        )
        self.client.login(username='testuser', password='Testpassword123')

    def test_user_list_view(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertContains(response, 'testuser')
