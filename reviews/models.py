from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Review(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_reviews"
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "reviewer")

    def __str__(self):
        return f"{self.reviewer.username} → {self.organizer.username}"