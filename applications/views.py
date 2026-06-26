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