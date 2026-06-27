from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from applications.models import Application
from django.contrib.auth.decorators import login_required


def create_event_view(request):

    if request.method == "POST":

        form = EventForm(request.POST)

        if form.is_valid():

            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            return redirect("/dashboard/")

    else:

        form = EventForm()

    return render(
        request,
        "events/create_event.html",
        {
            "form": form
        }
    )

def events_list_view(request):
    events = Event.objects.all().order_by("-created_at")

    return render(request, "events/events_list.html", {
        "events": events
    })

def event_details_view(request, event_id):
    event = Event.objects.get(id=event_id)

    user_application = None
    if request.user.is_authenticated:
        user_application = Application.objects.filter(
            event=event,
            applicant=request.user
        ).first()

    return render(request, "events/event_details.html", {
        "event": event,
        "user_application": user_application,
    })

@login_required
def my_events_view(request):

    events = Event.objects.filter(
        organizer=request.user
    ).order_by("-date_time")

    return render(
        request,
        "events/my_events.html",
        {
            "events": events
        }
    )

def edit_event_view(request, event_id):

    event = Event.objects.get(id=event_id)

    if event.organizer != request.user:
        return redirect(f"/events/{event.id}/")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect(f"/events/{event.id}/")

    else:
        form = EventForm(instance=event)

    return render(request, "events/edit_event.html", {
        "form": form,
        "event": event
    })

def delete_event_view(request, event_id):

    event = Event.objects.get(id=event_id)

    if event.organizer != request.user:
        return redirect(f"/events/{event.id}/")

    if request.method == "POST":
        event.delete()
        return redirect("/events/my/")

    return render(request, "events/delete_event.html", {
        "event": event
    })