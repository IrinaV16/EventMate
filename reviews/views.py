from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from events.models import Event
from applications.models import Application
from .models import Review
from .forms import ReviewForm
from notifications.models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def leave_review_view(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    application = Application.objects.filter(
        event=event,
        applicant=request.user,
        status="accepted"
    ).first()

    if not application:
        return redirect("event_details", event_id=event.id)

    if event.date_time > timezone.now():
        return redirect("event_details", event_id=event.id)

    if Review.objects.filter(
        event=event,
        reviewer=request.user
    ).exists():
        return redirect("event_details", event_id=event.id)

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

            return redirect("event_details", event_id=event.id)

    else:
        form = ReviewForm()

    return render(request, "reviews/leave_review.html", {
        "form": form,
        "event": event,
    })