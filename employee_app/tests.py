from django.test import TestCase

import datetime
from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse

from cinema_app.models import Movie
from .mixins import EMPLOYEE_GROUPS


class EmployeeAccessTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client_user = User.objects.create_user(username="client", password="motdepasse123")

        cls.group = Group.objects.create(name=EMPLOYEE_GROUPS[0])
        cls.group.permissions.add(
            Permission.objects.get(codename='view_movie'),
            Permission.objects.get(codename='add_movie'),
        )
        cls.employee = User.objects.create_user(username="employe", password="motdepasse123")
        cls.employee.groups.add(cls.group)

        cls.movie = Movie.objects.create(
            title="Alien", description="...", duration=117, release_date=datetime.date(1979, 5, 25),
        )

    def test_visiteur_redirige_vers_connexion(self):
        response = self.client.get(reverse('employee:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_client_refuse(self):
        self.client.force_login(self.client_user)
        response = self.client.get(reverse('employee:dashboard'))
        self.assertRedirects(response, reverse('index'))

    def test_employe_accede_au_dashboard(self):
        self.client.force_login(self.employee)
        response = self.client.get(reverse('employee:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_employe_voit_la_liste_des_films(self):
        self.client.force_login(self.employee)
        response = self.client.get(reverse('employee:movies'))
        self.assertContains(response, "Alien")

    def test_employe_sans_permission_ne_peut_pas_supprimer(self):
        self.client.force_login(self.employee)
        response = self.client.post(reverse('employee:movie_delete', args=[self.movie.pk]))
        self.assertTrue(Movie.objects.filter(pk=self.movie.pk).exists())
