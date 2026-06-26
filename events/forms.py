from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            "title",
            "description",
            "category",
            "location",
            "date_time",
            "max_participants",
            "is_adults_only",
        ]

        widgets = {
            "date_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            )
        }