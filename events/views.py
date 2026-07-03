from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from applications.models import Application
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from reviews.models import Review
import requests


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

    search_query = request.GET.get("search")
    category = request.GET.get("category")

    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if category:
        events = events.filter(category=category)

    return render(request, "events/events_list.html", {
        "events": events,
        "search_query": search_query,
        "category": category,
        "categories": Event.CATEGORY_CHOICES,
    })

def get_weather(location, event_date):

    try:
        today = timezone.now().date()
        days_until_event = (event_date.date() - today).days

        if days_until_event < 0 or days_until_event > 16:
            return None

        geocoding_url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={location}&count=1"
        )

        response = requests.get(geocoding_url)
        data = response.json()

        if "results" not in data:
            return None

        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]

        event_date_string = event_date.date().isoformat()

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code,wind_speed_10m_max"
            f"&start_date={event_date_string}"
            f"&end_date={event_date_string}"
        )

        response = requests.get(weather_url)
        weather = response.json()

        daily = weather["daily"]

        return {
            "max_temp": daily["temperature_2m_max"][0],
            "min_temp": daily["temperature_2m_min"][0],
            "wind_speed": daily["wind_speed_10m_max"][0],
            "weather_code": daily["weather_code"][0],
            "date": event_date_string,
        }

    except Exception:
        return None

def event_details_view(request, event_id):
    event = Event.objects.get(id=event_id)

    accepted_count = event.applications.filter(
        status="accepted"
    ).count()

    is_full = accepted_count >= event.max_participants

    user_application = None
    if request.user.is_authenticated:
        user_application = Application.objects.filter(
            event=event,
            applicant=request.user
        ).first()

    can_review = False

    if user_application and user_application.status == "accepted":
        if event.date_time <= timezone.now():
            if not Review.objects.filter(
                event=event,
                reviewer=request.user
            ).exists():
                can_review = True

    weather = get_weather(event.location, event.date_time)

    return render(request, "events/event_details.html", {
        "event": event,
        "user_application": user_application,
        "accepted_count": accepted_count,
        "is_full": is_full,
        "can_review": can_review,
        "weather": weather,
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