from django.test import TestCase
from django.contrib.auth.models import User
from .models import FriendRequest


class FriendRequestTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="ivan",
            password="12345678"
        )

        self.user2 = User.objects.create_user(
            username="maria",
            password="12345678"
        )

    def test_user_can_send_friend_request(self):

        self.client.login(
            username="ivan",
            password="12345678"
        )

        response = self.client.get(
            f"/friends/send/{self.user2.id}/"
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            FriendRequest.objects.filter(
                sender=self.user1,
                receiver=self.user2
            ).exists()
        )

    def test_user_can_accept_friend_request(self):

        friend_request = FriendRequest.objects.create(
            sender=self.user1,
            receiver=self.user2
        )

        self.client.login(
            username="maria",
            password="12345678"
        )

        response = self.client.get(
            f"/friends/accept/{friend_request.id}/"
        )

        friend_request.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(friend_request.status, "accepted")

    def test_user_can_reject_friend_request(self):

        friend_request = FriendRequest.objects.create(
            sender=self.user1,
            receiver=self.user2
        )

        self.client.login(
            username="maria",
            password="12345678"
        )

        response = self.client.get(
            f"/friends/reject/{friend_request.id}/"
        )

        friend_request.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(friend_request.status, "rejected")