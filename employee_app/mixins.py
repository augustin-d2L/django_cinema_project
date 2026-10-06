from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

EMPLOYEE_GROUPS = []


class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=EMPLOYEE_GROUPS).exists()

    def handle_no_permission(self):
        # Pas connecté : on laisse Django l'envoyer vers la page de connexion
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        # Connecté mais pas employé : message + retour à l'accueil
        messages.add_message(self.request, messages.ERROR, "Accès réservé aux employés.")
        return redirect('index')