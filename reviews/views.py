from django.shortcuts import render, redirect
from django.utils import timezone

from events.models import Event
from applications.models import Application

from .models import Review
from .forms import ReviewForm

from notifications.models import Notification


def leave_review_view(request, event_id):

    event = Event.objects.get(id=event_id)

    application = Application.objects.filter(
        event=event,
        applicant=request.user,
        status="accepted"
    ).first()

    if not application:
        return redirect(f"/events/{event.id}/")

    if event.date_time > timezone.now():
        return redirect(f"/events/{event.id}/")

    if Review.objects.filter(
        event=event,
        reviewer=request.user
    ).exists():
        return redirect(f"/events/{event.id}/")

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)
            review.event = event
            review.reviewer = request.user
            review.organizer = event.organizer
            review.save()

            Notification.objects.create(
                recipient=event.organizer,
                message=f"{request.user.username} left a review for your event '{event.title}'."
            )

            return redirect(f"/events/{event.id}/")

    else:
        form = ReviewForm()

    return render(request, "reviews/leave_review.html", {
        "form": form,
        "event": event,
    })