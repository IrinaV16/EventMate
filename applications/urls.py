from django.urls import path
from . import views

urlpatterns = [
    path("apply/<int:event_id>/", views.apply_for_event, name="apply_for_event"),
]