from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_event_view, name="create_event"),
    path("my/", views.my_events_view, name="my_events"),
    path("", views.events_list_view, name="events_list"),
    path("<int:event_id>/edit/", views.edit_event_view, name="edit_event"),
    path("<int:event_id>/delete/", views.delete_event_view, name="delete_event"),
    path("<int:event_id>/", views.event_details_view, name="event_details"),
]