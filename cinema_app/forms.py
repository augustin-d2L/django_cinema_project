from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, CinemaRoom
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

import datetime

HEURE_CHOICES = [(f"{h:02d}:00", f"{h:02d}h00") for h in range(8, 23)]

class ContactForm(forms.Form):
    email_address = forms.EmailField(
        label=_("Adresse Courriel"),
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red',
            'placeholder': 'vous@exemple.com'
        })
    )
    message_content = forms.CharField(
        label=_("Message"),
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red resize-none',
            'rows': 5,
            'placeholder': 'Votre message...'
        })
    )


class ReservationForm(forms.Form):
    hour = forms.ChoiceField(
        label=_("Heure"),
        choices=HEURE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    film = forms.ModelChoiceField(
        label=_("Film"),
        queryset=Movie.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    room = forms.ModelChoiceField(
        label=_("Salle"),
        queryset=CinemaRoom.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    date = forms.DateField(
        label=_("Date"),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )
    seat_number = forms.CharField(
        label=_("Numéro de siège"),
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red',
            'placeholder': 'ex. A12'
        })
    )

    def clean_date(self):
        date_value = self.cleaned_data.get('date')
        if date_value and date_value < datetime.date.today():
            raise ValidationError("La date ne peut pas être dans le passé")
        return date_value


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password']:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-cinema-red'
            })


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Adresse courriel"),
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
            })


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md bg-white/5 border border-white/10 text-white focus:outline-none focus:border-cinema-red'
            }),
        }