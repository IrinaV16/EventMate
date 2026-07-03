from django.urls import path
from . import views

urlpatterns = [
    path("", views.friends_view, name="friends"),
    path("send/<int:user_id>/", views.send_friend_request, name="send_friend_request"),
    path("accept/<int:request_id>/", views.accept_friend_request, name="accept_friend_request"),
    path("reject/<int:request_id>/", views.reject_friend_request, name="reject_friend_request"),
]