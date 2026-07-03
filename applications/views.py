from django.shortcuts import render

from django.shortcuts import redirect
from events.models import Event
from .models import Application
from notifications.models import Notification


def apply_for_event(request, event_id):
    event = Event.objects.get(id=event_id)

    accepted_count = event.applications.filter(
        status="accepted"
    ).count()

    if accepted_count >= event.max_participants:
        return redirect(f"/events/{event.id}/")

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

    return redirect(f"/events/{event.id}/")

def accept_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.event.organizer == request.user:
        application.status = "accepted"
        application.save()

        Notification.objects.create(
            recipient=application.applicant,
            message=f"Your application for '{application.event.title}' was accepted."
        )

    return redirect(f"/events/{application.event.id}/")


def reject_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.event.organizer == request.user:
        application.status = "rejected"
        application.save()

        Notification.objects.create(
            recipient=application.applicant,
            message=f"Your application for '{application.event.title}' was rejected."
        )

    return redirect(f"/events/{application.event.id}/")

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