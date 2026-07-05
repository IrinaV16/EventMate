from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Event
from .models import Application

class ApplicationTest(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="organizer",
            password="12345678"
        )

        self.applicant = User.objects.create_user(
            username="applicant",
            password="12345678"
        )

        self.event = Event.objects.create(
            organizer=self.organizer,
            title="Hiking",
            description="Mountain trip",
            category="hiking",
            location="Sofia",
            date_time=timezone.now() + timedelta(days=3),
            max_participants=5,
            is_adults_only=False,
        )

    def test_user_can_apply_for_event(self):
        self.client.login(
            username="applicant",
            password="12345678"
        )

        response = self.client.get(f"/applications/apply/{self.event.id}/")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Application.objects.filter(
                event=self.event,
                applicant=self.applicant
            ).exists()
        )

    def test_user_cannot_apply_twice(self):

        self.client.login(
            username="applicant",
            password="12345678"
        )

        self.client.get(f"/applications/apply/{self.event.id}/")
        self.client.get(f"/applications/apply/{self.event.id}/")

        self.assertEqual(
            Application.objects.filter(
                event=self.event,
                applicant=self.applicant
            ).count(),
            1
        )

    def test_organizer_can_accept_application(self):

        application = Application.objects.create(
            event=self.event,
            applicant=self.applicant
        )

        self.client.login(
            username="organizer",
            password="12345678"
        )

        response = self.client.get(
            f"/applications/accept/{application.id}/"
        )

        application.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(application.status, "accepted")

    def test_organizer_can_reject_application(self):

        application = Application.objects.create(
            event=self.event,
            applicant=self.applicant
        )

        self.client.login(
            username="organizer",
            password="12345678"
        )

        response = self.client.get(
            f"/applications/reject/{application.id}/"
        )

        application.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(application.status, "rejected")