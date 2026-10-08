from django.shortcuts import render
from django.views import View
from .mixins import EmployeeRequiredMixin

#TODO : mettre dans toutes les classes de vues le mixin EmployeeRequiredMixin pour restreindre l'accès aux employés
class DashboardView(EmployeeRequiredMixin, View):
    def get(self, request):
        return render(request, 'employee_app/dashboard.html')