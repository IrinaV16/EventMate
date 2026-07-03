from django.shortcuts import render, redirect, get_object_or_404
from events.models import Event
from .models import Application
from notifications.models import Notification
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def apply_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.date_time <= timezone.now():
        return redirect("event_details", event_id=event.id)

    accepted_count = event.applications.filter(
        status="accepted"
    ).count()

    if accepted_count >= event.max_participants:
        return redirect("event_details", event_id=event.id)

    if event.organizer != request.user:
        application, created = Application.objects.get_or_create(
            event=event,
            applicant=request.user
        )

        if created:
            Notification.objects.create(
                recipient=event.organizer,
                message=f"{request.user.username} applied for your event '{event.title}'."
        )

    return redirect("event_details", event_id=event.id)

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if application.event.organizer == request.user:
        application.status = "accepted"
        application.save()

        Notification.objects.create(
            recipient=application.applicant,
            message=f"Your application for '{application.event.title}' was accepted."
        )

    return redirect("event_details", event_id=application.event.id)

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if application.event.organizer == request.user:
        application.status = "rejected"
        application.save()

        Notification.objects.create(
            recipient=application.applicant,
            message=f"Your application for '{application.event.title}' was rejected."
        )

    return redirect("event_details", event_id=application.event.id)

@login_required
def my_applications_view(request):

    applications = Application.objects.filter(
        applicant=request.user
    ).order_by("-created_at")

    return render(
        request,
        "applications/my_applications.html",
        {
            "applications": applications
        }
    )