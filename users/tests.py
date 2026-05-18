from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCrudTastCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "john",
            "password": "secretpassword",
            "first_name": "John",
            "last_name": "Johns",
        }
        self.user = User.objects.create_user(**self.user_data)

        self.new_user_data = {
            "username": "jane",
            "password1": "janepassword",
            "password2": "janepassword",
            "first_name": "Jane",
            "last_name": "Doe",
        }

    def test_users_list(self):
        url = reverse("users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_create_user(self):
        url = reverse("user_create")
        response = self.client.post(url, self.new_user_data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="jane").exists())

    def test_login_logout(self):
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            {
                "username": "john",
                "password": "secretpassword",
            },
        )
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)
        logout_url = reverse("logout")
        response = self.client.post(logout_url)
        self.assertRedirects(response, reverse("index"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_update(self):
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        url = reverse("user_update", kwargs={"pk": self.user.id})
        updated_data = {
            "username": "john_new",
            "first_name": "Johnny",
            "last_name": "Johns",
        }
        response = self.client.post(url, updated_data)
        self.assertRedirects(response, reverse("users"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Johnny")
        self.assertEqual(self.user.last_name, "Johns")

    def test_update_other_user(self):
        other_user = User.objects.create_user(username="other", password="123")
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        url = reverse("user_update", kwargs={"pk": other_user.id})
        response = self.client.post(url, {"username": "hacker"})
        self.assertRedirects(response, reverse("users"))
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.username, "hacker")

    def test_delete_user(self):
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        url = reverse("user_delete", kwargs={"pk": self.user.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users"))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_other_user(self):
        other_user = User.objects.create_user(username="other", password="123")
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password"]
        )
        url = reverse("user_delete", kwargs={"pk": other_user.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users"))
        self.assertTrue(User.objects.filter(id=other_user.id).exists())
