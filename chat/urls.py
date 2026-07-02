from django.urls import path
from . import views

urlpatterns = [
    path("event/<int:event_id>/", views.event_chat_view, name="event_chat"),
]