from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task
from statuses.models import Status
from django.contrib.auth.models import User
from django.db.models import ProtectedError


class TaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            password='secretpassword',
            first_name='John',
            last_name='Johns'
        )

        self.other_user = User.objects.create_user(
            username='jane',
            password='janepassword'
        )

        self.status = Status.objects.create(name='Новый')

        self.task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.user,
            executor=self.other_user
        )


    def tesr_tasks_access(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='john', password='secretpassword')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)


    def test_create_task(self):
        self.client.login(username='john', password='secretpassword')
        url = reverse('task_create')
        data ={
            'name': 'New Task',
            'description': 'Some description',
            'status': self.status.id,
            'executor': self.other_user.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('tasks'))

        new_task = Task.objects.get(name='New Task')
        self.assertEqual(new_task.author, self.user)
        self.assertEqual(new_task.executor, self.other_user)


    def test_update_task(self):
        self.client.login(username='john', password='secretpassword')
        url = reverse('task_update', kwargs={'pk':self.task.id})
        data = {
            'name': 'Обновленная задача',
            'status': self.status.id,
            'executor': self.other_user.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')


    def test_delete_task_by_author(self):
        self.client.login(username='john', password='secretpassword')
        url = reverse('task_delete', kwargs={'pk':self.task.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


    def test_delete_task_non_author(self):
        self.client.login(username='jane', password='janepassword')
        url = reverse('task_delete', kwargs={'pk': self.task.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_user_deletion_with_tasks(self):
        with self.assertRaises(ProtectedError):
            self.user.delete()