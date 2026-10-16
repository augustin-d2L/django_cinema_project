from django.test import TestCase

import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.utils import timezone

from .forms import ReservationForm
from .models import CinemaRoom, Genre, Movie, Screening, Ticket


class ModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(name="Horreur")
        cls.movie = Movie.objects.create(
            title="Alien", description="Dans l'espace...",
            duration=117, release_date=datetime.date(1979, 5, 25), genre=cls.genre,
        )
        cls.room = CinemaRoom.objects.create(number=1, capacity=100)
        cls.screening = Screening.objects.create(
            movie=cls.movie, cinema_room=cls.room,
            screening_time=timezone.now() + datetime.timedelta(days=1),
        )
        cls.user = User.objects.create_user(username="client", password="motdepasse123")

    def test_str_du_film(self):
        self.assertEqual(str(self.movie), "Alien")

    def test_un_siege_ne_peut_pas_etre_reserve_deux_fois(self):
        Ticket.objects.create(screening=self.screening, person=self.user, price=12.50, seat_number="A1")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Ticket.objects.create(screening=self.screening, person=self.user, price=12.50, seat_number="A1")


class ReservationFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie.objects.create(
            title="Alien", description="...", duration=117, release_date=datetime.date(1979, 5, 25),
        )
        cls.room = CinemaRoom.objects.create(number=1, capacity=100)

    def _data(self, date):
        return {
            'film': self.movie.pk, 'room': self.room.pk,
            'date': date, 'hour': '15:00', 'seat_number': 'A1',
        }

    def test_date_passee_refusee(self):
        hier = datetime.date.today() - datetime.timedelta(days=1)
        form = ReservationForm(data=self._data(hier))
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_date_future_acceptee(self):
        demain = datetime.date.today() + datetime.timedelta(days=1)
        form = ReservationForm(data=self._data(demain))
        self.assertTrue(form.is_valid(), form.errors)


class PublicPagesTests(TestCase):

    def test_pages_publiques_accessibles(self):
        for name in ['index', 'movies', 'contact', 'register']:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_film_inexistant_renvoie_404(self):
        response = self.client.get(reverse('movie', args=[9999]))
        self.assertEqual(response.status_code, 404)


class LoginRequiredTests(TestCase):

    def test_reservation_redirige_vers_connexion(self):
        response = self.client.get(reverse('reservation'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('reservation')}")

    def test_compte_redirige_vers_connexion(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_compte_accessible_une_fois_connecte(self):
        user = User.objects.create_user(username="client", password="motdepasse123")
        self.client.force_login(user)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)