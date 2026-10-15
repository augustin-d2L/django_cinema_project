from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('/movies', views.MoviesManagementView.as_view(), name='movies')
]