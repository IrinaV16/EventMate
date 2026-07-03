from django.test import TestCase
from django.contrib.auth.models import User

from .models import Notification


class NotificationTest(TestCase):

    def test_notification_can_be_created(self):

        user = User.objects.create_user(
            username="ivan",
            password="12345678"
        )

        notification = Notification.objects.create(
            recipient=user,
            message="Test notification"
        )

        self.assertEqual(notification.recipient, user)
        self.assertEqual(notification.message, "Test notification")