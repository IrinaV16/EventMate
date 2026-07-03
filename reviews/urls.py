from django.urls import path
from . import views

urlpatterns = [
    path("leave/<int:event_id>/", views.leave_review_view, name="leave_review"),
]