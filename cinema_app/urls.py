from django.urls import path

from . import views

# revoir exemple demo_app
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]