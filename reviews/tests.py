from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from events.models import Event
from applications.models import Application
from .models import Review

class ReviewTest(TestCase):

    def setUp(self):

        self.organizer = User.objects.create_user(
            username="organizer",
            password="12345678"
        )

        self.user = User.objects.create_user(
            username="reviewer",
            password="12345678"
        )

        self.event = Event.objects.create(
            organizer=self.organizer,
            title="Hiking",
            description="Trip",
            category="hiking",
            location="Plovdiv",
            date_time=timezone.now() - timedelta(days=1),
            max_participants=5,
            is_adults_only=False,
        )

        Application.objects.create(
            event=self.event,
            applicant=self.user,
            status="accepted"
        )

    def test_accepted_user_can_leave_review(self):

        self.client.login(
            username="reviewer",
            password="12345678"
        )

        response = self.client.post(
            f"/reviews/leave/{self.event.id}/",
            {
                "rating": 5,
                "comment": "Great event!"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Review.objects.filter(
                event=self.event,
                reviewer=self.user
            ).exists()
        )

    def test_user_cannot_leave_second_review(self):

        Review.objects.create(
            event=self.event,
            reviewer=self.user,
            organizer=self.organizer,
            rating=5,
            comment="Great!"
        )

        self.client.login(
            username="reviewer",
            password="12345678"
        )

        response = self.client.post(
            f"/reviews/leave/{self.event.id}/",
            {
                "rating": 4,
                "comment": "Another review"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Review.objects.filter(
                event=self.event,
                reviewer=self.user
            ).count(),
            1
        )