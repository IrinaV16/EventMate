from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("sport", "Sport"),
        ("party", "Party"),
        ("festival", "Festival"),
        ("hiking", "Hiking"),
        ("cinema", "Cinema"),
        ("concert", "Concert"),
        ("games", "Board Games"),
        ("other", "Other"),
    ]

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events"
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    location = models.CharField(max_length=150)
    date_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    is_adults_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title