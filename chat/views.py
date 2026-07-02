from django.shortcuts import render, redirect
from events.models import Event
from applications.models import Application
from .models import ChatMessage


def event_chat_view(request, event_id):
    event = Event.objects.get(id=event_id)

    is_organizer = event.organizer == request.user

    is_accepted = Application.objects.filter(
        event=event,
        applicant=request.user,
        status="accepted"
    ).exists()

    if not is_organizer and not is_accepted:
        return redirect(f"/events/{event.id}/")

    messages = ChatMessage.objects.filter(
        event=event
    ).order_by("created_at")

    return render(request, "chat/event_chat.html", {
        "event": event,
        "messages": messages
    })