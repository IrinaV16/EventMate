from django.shortcuts import render

from django.shortcuts import redirect
from events.models import Event
from .models import Application


def apply_for_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if event.organizer != request.user:
        Application.objects.get_or_create(
            event=event,
            applicant=request.user
        )

    return redirect(f"/events/{event.id}/")

def accept_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.event.organizer == request.user:
        application.status = "accepted"
        application.save()

    return redirect(f"/events/{application.event.id}/")


def reject_application(request, application_id):
    application = Application.objects.get(id=application_id)

    if application.event.organizer == request.user:
        application.status = "rejected"
        application.save()

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