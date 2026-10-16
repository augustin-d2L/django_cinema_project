from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

EMPLOYEE_GROUPS = ['réceptionniste', 'administrateur']


def is_employee(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name__in=EMPLOYEE_GROUPS).exists()
    )


class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        return is_employee(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.add_message(self.request, messages.ERROR, _("Accès réservé aux employés."))
        return redirect('index')


class EmployeePermissionMixin(PermissionRequiredMixin):
    login_url = 'login'

    def handle_no_permission(self):
        user = self.request.user
        if not user.is_authenticated:
            return super().handle_no_permission()
        if is_employee(user):
            messages.add_message(self.request, messages.ERROR, _("Vous n'avez pas la permission d'effectuer cette action."))
            return redirect('employee:dashboard')
        messages.add_message(self.request, messages.ERROR, _("Accès réservé aux employés."))
        return redirect('index')