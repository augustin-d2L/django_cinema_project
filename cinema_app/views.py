from django.shortcuts import redirect, render
#from django.http import Http404 voir demo_app
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.contrib import messages
from .models import * # a changer
from .forms import ContactForm, ReservationForm, RegisterForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

#TODO : être authentifié pour faire une reservation utilisation de User
#TODO : quand on clique sur reserver depuis un film on préremplis le formulaire avec lui
#TODO : mettre try except pour chaque interaction DB
#TODO movieView : si le film n'existe pas erreur releve utiliser try except DoesNotExist 

class IndexView(View):
    def get(self, request):
        return render(request, 'cinema_app/index.html')


class ReservationView(LoginRequiredMixin, View):
    login_url = 'login'  # redirige ici si pas connecté

    def get(self, request):
        form = ReservationForm()
        return render(request, 'cinema_app/reservation.html', {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()

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


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Compte créé avec succès !")
            return redirect('index')

        return render(request, 'registration/register.html', {'form': form})


class AccountView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        reservations = request.user.reservations.all().order_by('date', 'hour')
        return render(request, 'cinema_app/account.html', {
            'form': form,
            'reservations': reservations,
        })

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profil mis à jour.")
            return redirect('account')

        reservations = request.user.reservations.all().order_by('date', 'hour')
        return render(request, 'cinema_app/account.html', {
            'form': form,
            'reservations': reservations,
        })


class DeleteReservationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        return render(request, 'cinema_app/delete_reservation_confirm.html', {'reservation': reservation})

    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

        if reservation.is_past():
            messages.add_message(request, messages.ERROR, "Impossible de supprimer une réservation passée.")
            return redirect('account')

        reservation.delete()
        messages.add_message(request, messages.SUCCESS, "Réservation annulée.")
        return redirect('account')