from django.test import TestCase
from django.contrib.auth.models import User


class AccountsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="irina",
            password="12345678"
        )

    def test_user_can_login(self):

        response = self.client.post("/login/", {
            "username": "irina",
            "password": "12345678"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/dashboard/")

    def test_anonymous_user_cannot_access_dashboard(self):

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)