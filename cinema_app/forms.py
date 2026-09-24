from django import forms
from django.core.exceptions import ValidationError
from .models import Movie, CinemaRoom

import datetime

HEURE_CHOICES = [(f"{h:02d}:00", f"{h:02d}h00") for h in range(8, 23)]

class ContactForm(forms.Form):
    email_address = forms.EmailField(
        label="Adresse Courriel",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red',
            'placeholder': 'vous@exemple.com'
        })
    )
    message_content = forms.CharField(
        label="Message",
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red resize-none',
            'rows': 5,
            'placeholder': 'Votre message...'
        })
    )


class ReservationForm(forms.Form):
    email_address = forms.EmailField(
        label="Adresse Courriel",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red'
        })
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red'
        })
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red'
        })
    )
    date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    hour = forms.ChoiceField(
        label="Heure",
        choices=HEURE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    film = forms.ModelChoiceField(
        label="Film",
        queryset=Movie.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    room = forms.ModelChoiceField(
        label="Salle",
        queryset=CinemaRoom.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )

    def clean_date(self):
        date_value = self.cleaned_data.get('date')

        if date_value and date_value < datetime.date.today():
            raise ValidationError("La date ne peut pas être dans le passé")

        return date_value