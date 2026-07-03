from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Event
from .forms import EventForm


class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345678"
        )

    def test_create_event(self):

        event = Event.objects.create(
            organizer=self.user,
            title="Football",
            description="Friendly match",
            category="sports",
            location="Plovdiv",
            date_time=timezone.now() + timedelta(days=5),
            max_participants=10,
            is_adults_only=False,
        )

        self.assertEqual(event.title, "Football")
        self.assertEqual(event.organizer, self.user)
        self.assertEqual(event.location, "Plovdiv")

        

    def test_event_date_cannot_be_in_the_past(self):

            form_data = {
                "title": "Past Event",
                "description": "This should not be valid",
                "category": "sports",
                "location": "Sofia",
                "date_time": timezone.now() - timedelta(days=1),
                "max_participants": 10,
                "is_adults_only": False,
            }

            form = EventForm(data=form_data)

            self.assertFalse(form.is_valid())
            self.assertIn("date_time", form.errors)

    def test_logged_in_user_can_create_event(self):

        self.client.login(
            username="testuser",
            password="12345678"
        )

        response = self.client.post("/events/create/", {
            "title": "Cinema Night",
            "description": "Watching a movie",
            "category": "party",
            "location": "Sofia",
            "date_time": (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
            "max_participants": 5,
            "is_adults_only": False,
        })

        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_create_event(self):

        response = self.client.get("/events/create/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        
