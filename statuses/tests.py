from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status

class StatusTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'john',
            'password': 'secretpassword',
            'first_name': 'John',
            'last_name': 'Johns'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.status = Status.objects.create(name='New')


    def test_statuses_list_access(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='john', password='secretpassword')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)


    def test_create_status(self):
        self.client.login(username='john', password='secretpassword')
        response = self.client.post(reverse('status_create'), {'name': 'status1'})
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name= 'status1').exists())


    def test_update_status(self):
        self.client.login(username='john', password='secretpassword')
        url = reverse('status_update', kwargs={'pk': self.status.id})
        response = self.client.post(url, {'name': 'test1'})
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'test1')


    def test_delete_status(self):
        self.client.login(username='john', password='secretpassword')
        url = reverse('status_delete', kwargs={'pk': self.status.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(pk=self.status.id).exists())
