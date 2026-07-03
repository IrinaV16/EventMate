from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from events.models import Event
from .models import ChatMessage


class ChatTest(TestCase):

    def test_chat_message_can_be_created(self):

        user = User.objects.create_user(
            username="ivan",
            password="12345678"
        )

        event = Event.objects.create(
            organizer=user,
            title="Football",
            description="Match",
            category="sports",
            location="Plovdiv",
            date_time=timezone.now() + timedelta(days=1),
            max_participants=10,
            is_adults_only=False,
        )

        message = ChatMessage.objects.create(
            event=event,
            sender=user,
            message="Hello!"
        )

        self.assertEqual(message.sender, user)
        self.assertEqual(message.event, event)
        self.assertEqual(message.message, "Hello!")