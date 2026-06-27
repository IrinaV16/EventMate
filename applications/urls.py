from django.urls import path
from . import views

urlpatterns = [
    path("my/", views.my_applications_view, name="my_applications"),
    path("apply/<int:event_id>/", views.apply_for_event, name="apply_for_event"),
    path("accept/<int:application_id>/", views.accept_application, name="accept_application"),
    path("reject/<int:application_id>/", views.reject_application, name="reject_application"),
]