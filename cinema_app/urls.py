from django.urls import path

from . import views

# revoir exemple demo_app
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('movies', views.MoviesView.as_view(), name='movies'),
    path('movie/<int:pk>', views.MovieView.as_view(), name='movie'),
]