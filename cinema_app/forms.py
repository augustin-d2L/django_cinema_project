from django import forms
from django.core.exceptions import ValidationError
from .models import Movie, CinemaRoom

import datetime

HEURE_CHOICES = [(f"{h:02d}:00", f"{h:02d}h00") for h in range(8, 23)]

class ContactForm(forms.Form):
    email_address = forms.EmailField(label="Adresse Courriel")
    message_content = forms.CharField(label="Message", max_length=500, widget=forms.Textarea)


class ReservationForm(forms.Form):
    email_address = forms.EmailField(label="Adresse Courriel")
    first_name = forms.CharField(label="Prénom", max_length=50)
    last_name = forms.CharField(label="Nom", max_length=50)
    date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={'type': 'date'}),

    )
    hour = forms.ChoiceField(label="Heure", choices=HEURE_CHOICES)
    film = forms.ModelChoiceField(
        label="Film",
        queryset=Movie.objects.all()
    )
    room = forms.ModelChoiceField(
        label="Salle",
        queryset=CinemaRoom.objects.all()
    )

    def clean_date(self):
        date_value = self.cleaned_data.get('date')

        if date_value and date_value < datetime.date.today():
            raise ValidationError("La date ne peut pas être dans le passé")

        return date_value
    