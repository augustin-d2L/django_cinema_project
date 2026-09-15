from django.contrib import admin
from .models import Genre, Movie, CinemaRoom, Screening, Ticket, Person

# voirce au'on peut faire avec l'admin de django demo_app
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(CinemaRoom)
admin.site.register(Screening)
admin.site.register(Ticket)
admin.site.register(Person)