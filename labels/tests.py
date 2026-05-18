from django.test import TestCase
from django.urls import reverse
from labels.models import Label
from django.contrib.auth.models import User


class LabelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="secretpassword",
            first_name="John",
            last_name="Johns",
        )
        self.client.login(username="john", password="secretpassword")
        self.label = Label.objects.create(name="Bug")

    def test_label_list(self):
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/index.html")

    def test_label_create(self):
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("label_create"), {"name": "Feature"})
        self.assertRedirects(response, reverse("labels"))
        self.assertTrue(Label.objects.filter(name="Feature").exists())

    def test_label_update(self):
        response = self.client.get(
            reverse("label_update", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 200)
        url = reverse("label_update", kwargs={"pk": self.label.id})
        response = self.client.post(url, {"name": "Fixed"})
        self.assertRedirects(response, reverse("labels"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Fixed")

    def test_label_delete(self):
        response = self.client.get(
            reverse("label_delete", kwargs={"pk": self.label.id})
        )
        self.assertEqual(response.status_code, 200)
        url = reverse("label_delete", kwargs={"pk": self.label.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("labels"))
        self.assertFalse(Label.objects.filter(name="Bug").exists())

    def test_label_delete_without_tasks(self):
        self.client.logout()
        urls = [
            reverse("labels"),
            reverse("label_create"),
            reverse("label_update", kwargs={"pk": self.label.id}),
            reverse("label_delete", kwargs={"pk": self.label.id}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login page
