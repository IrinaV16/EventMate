from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from events.models import Event

def home(request):
    return render(request, "accounts/home.html")

def login_view(request):

    error_message = None

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        else:
            error_message = "Invalid username or password."

    return render(request, "accounts/login.html", {
        "error_message": error_message
    })

def register_view(request):


    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error_message": "Username already exists."
            })

        if password1 != password2:
            return render(request, "accounts/register.html", {
                "error_message": "Passwords do not match."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        Profile.objects.create(user=user)

        return redirect("/login/")

    return render(request, "accounts/register.html")

def dashboard_view(request):

    events = Event.objects.order_by("-created_at")[:3]

    my_events = Event.objects.filter(
        organizer=request.user
    )

    return render(
        request,
        "accounts/dashboard.html",
        {
            "events": events,
            "my_events": my_events,
        }
    )

def logout_view(request):
    logout(request)
    return redirect("/")

def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(request, "accounts/profile.html", {
        "profile": profile
    })