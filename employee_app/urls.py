from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('films', views.MovieListView.as_view(), name='movies'),
    path('film/ajouter', views.MovieCreateView.as_view(), name='movie_add'),
    path('film/<int:pk>/supprimer', views.MovieDeleteView.as_view(), name='movie_delete'),
    path('film/<int:pk>/modifier', views.MovieUpdateView.as_view(), name='movie_add')
]