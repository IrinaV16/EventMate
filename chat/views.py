from django.shortcuts import render, redirect, get_object_or_404
from events.models import Event
from applications.models import Application
from .models import ChatMessage
from django.contrib.auth.decorators import login_required

@login_required
def event_chat_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    is_organizer = event.organizer == request.user

    is_accepted = Application.objects.filter(
        event=event,
        applicant=request.user,
        status="accepted"
    ).exists()

    if not is_organizer and not is_accepted:
        return redirect("event_details", event_id=event.id)

    messages = ChatMessage.objects.filter(
        event=event
    ).order_by("created_at")

    return render(request, "chat/event_chat.html", {
        "event": event,
        "messages": messages
    })