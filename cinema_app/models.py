from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = "genre"
        verbose_name_plural = "genres"

class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    duration = models.PositiveIntegerField(verbose_name="Durée (minutes)")
    release_date = models.DateField(verbose_name="Date de sortie")
    genre = models.ManyToManyField(Genre, verbose_name="Genre", related_name='movies', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )
        verbose_name = "film"
        verbose_name_plural = "films"

class CinemaRoom(models.Model):
    number = models.PositiveIntegerField(verbose_name="Numéro", unique=True)
    capacity = models.PositiveIntegerField(verbose_name="Capacité")

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ('number', )
        verbose_name = "salle de cinéma"
        verbose_name_plural = "salles de cinéma"

class Screening(models.Model): # Careful to not overlap 2 screenings in same room at same time
    movie = models.ForeignKey(Movie, verbose_name="Film", related_name='screenings', on_delete=models.CASCADE)
    cinema_room = models.ForeignKey('CinemaRoom', verbose_name="Salle de cinéma", related_name='screenings', on_delete=models.CASCADE)
    screening_time = models.DateTimeField(verbose_name="Heure de projection")

    def __str__(self):
        return f"{self.movie.title} - {self.screening_time}"

    class Meta:
        ordering = ('screening_time', )
        verbose_name = "projection"
        verbose_name_plural = "projections"

class Ticket(models.Model):
    class Status(models.TextChoices):
        RESERVED = 'RE', 'Réservé'
        PAID = 'PA', 'Payé'
        CANCELLED = 'CA', 'Annulé'

    screening = models.ForeignKey(Screening, verbose_name="Projection", related_name='tickets', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prix")
    seat_number = models.CharField(max_length=10, verbose_name="Siège")
    person = models.ForeignKey(User, verbose_name="Acheteur", related_name='tickets', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.RESERVED, verbose_name="Statut")

    def __str__(self):
        return f"{self.screening.movie.title} | {self.screening.screening_time}, {self.screening.cinema_room} - {self.seat_number}"

    class Meta:
        ordering = ('screening', 'seat_number',)
        verbose_name = "billet"
        verbose_name_plural = "billets"
        constraints = [
            models.UniqueConstraint(fields=['screening', 'seat_number'], name='unique_seat_per_screening')
        ]