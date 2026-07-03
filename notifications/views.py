from django.shortcuts import render
from .models import Notification


def notifications_view(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    return render(request, "notifications/notifications.html", {
        "notifications": notifications
    })