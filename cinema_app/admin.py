from django.contrib import admin
from .models import Genre, Movie, CinemaRoom, Screening, Ticket, ContactMessage

#TODO : personnaliser l'affichage

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(CinemaRoom)
admin.site.register(Screening)
admin.site.register(Ticket)
admin.site.register(ContactMessage)