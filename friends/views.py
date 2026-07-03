from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import FriendRequest
from notifications.models import Notification

from django.db.models import Q


def send_friend_request(request, user_id):
    receiver = User.objects.get(id=user_id)

    if receiver != request.user:
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver
        )

        if created:
            Notification.objects.create(
                recipient=receiver,
                message=f"{request.user.username} sent you a friend request."
            )

    return redirect(f"/profile/{receiver.id}/")


def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)

    if friend_request.receiver == request.user:
        friend_request.status = "accepted"
        friend_request.save()

        Notification.objects.create(
            recipient=friend_request.sender,
            message=f"{request.user.username} accepted your friend request."
        )

    return redirect("/friends/")


def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)

    if friend_request.receiver == request.user:
        friend_request.status = "rejected"
        friend_request.save()

    return redirect("/friends/")

def friends_view(request):

    pending_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status="pending"
    )

    friends = FriendRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status="accepted"
    )

    return render(
        request,
        "friends/friends.html",
        {
            "pending_requests": pending_requests,
            "friends": friends,
        }
    )