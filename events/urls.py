from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_event_view, name="create_event"),
    path("", views.events_list_view, name="events_list"),
    path("<int:event_id>/", views.event_details_view, name="event_details"),
]