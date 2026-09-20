from django.shortcuts import render
#from django.http import Http404 voir demo_app
from django.views.generic.base import View

class IndexView(View):
    def get(self, request):
        return render(request, 'cinema_app/index.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'cinema_app/contact.html')

class MoviesView(View):
    def get(self, request):
        return render(request, 'cinema_app/movies.html')