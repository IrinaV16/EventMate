from django import forms
from .models import Event
from django.utils import timezone


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

        help_texts = {
            "location": (
                "ℹ️ Enter a city or well-known place "
                "(e.g. Sofia, Plovdiv, Vitosha Mountain) "
                "for accurate weather forecasts."
            ),
        }

    def clean_date_time(self):
        date_time = self.cleaned_data["date_time"]

        if date_time <= timezone.now():
            raise forms.ValidationError(
                "The event date must be in the future."
            )

        return date_time