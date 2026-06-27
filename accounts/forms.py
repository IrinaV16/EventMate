from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "bio",
            "location",
            "interests",
            "profile_picture",
        ]