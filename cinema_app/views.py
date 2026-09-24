from django.shortcuts import redirect, render
#from django.http import Http404 voir demo_app
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.contrib import messages
from .models import * # a changer
from .forms import ContactForm, ReservationForm

#TODO : être authentifié pour faire une reservation utilisation de User
#TODO : quand on clique sur reserver depuis un film on préremplis le formulaire avec lui
#TODO : mettre try except pour chaque interaction DB
#TODO movieView : si le film n'existe pas erreur releve utiliser try except DoesNotExist 

class IndexView(View):
    def get(self, request):
        return render(request, 'cinema_app/index.html')


class ReservationView(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'cinema_app/reservation.html', {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            #TODO creer la projection

            messages.add_message(request, messages.SUCCESS, "Réservation bien effectuée")
            return redirect('index')

        return render(request, 'cinema_app/reservation.html', {'form': form})

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'cinema_app/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            contact_message = ContactMessage(email_address=form['email_address'], message_content=form['message_content'])
            contact_message.save()

            messages.add_message(request, messages.SUCCESS, "Message bien envoyé")
            return redirect('contact')

        return render(request, 'cinema_app/contact.html', {'form': form})


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
        movie = Movie.objects.prefetch_related('genre').get(pk=pk) 
        return render(request, 'cinema_app/movie.html', {'movie': movie})