from django.urls import path

from . import views

# revoir exemple demo_app
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('reservation', views.ReservationView.as_view(), name='reservation'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('movies', views.MoviesView.as_view(), name='movies'),
    path('movie/<int:pk>', views.MovieView.as_view(), name='movie'),
    path('inscription', views.RegisterView.as_view(), name='register'),
    path('compte', views.AccountView.as_view(), name='account'),
    path('compte/reservation/<int:pk>/supprimer', views.DeleteReservationView.as_view(), name='delete_reservation'),
]