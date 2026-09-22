from django.shortcuts import render
#from django.http import Http404 voir demo_app
from django.views.generic.base import View
from django.core.paginator import Paginator
from .models  import * # a changer

class IndexView(View):
    def get(self, request):
        return render(request, 'cinema_app/index.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'cinema_app/contact.html')


class MoviesView(View):
    model = Movie

    def get(self, request):
        movies = Movie.objects.prefetch_related('genre').all().reverse()
        paginator = Paginator(movies, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'cinema_app/movies.html', {'page': page_obj})


class MovieView(View):
    model = Movie

    def get(self, request, pk):
        movie = Movie.objects.prefetch_related('genre').get(pk=pk) # si le film n'existe pas erreur releve utiliser try except DoesNotExist 
        return render(request, 'cinema_app/movie.html', {'movie': movie})