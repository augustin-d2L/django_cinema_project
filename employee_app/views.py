from django.shortcuts import render
from django.views import View
from .mixins import EmployeeRequiredMixin

class DashboardView(EmployeeRequiredMixin, View):
    def get(self, request):
        return render(request, 'employee_app/dashboard.html')