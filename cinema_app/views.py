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
import datetime
from .constants import PRIX_BILLET
from employee_app.mixins import EMPLOYEE_GROUPS
from django.utils import timezone
from django.utils.translation import gettext as _


#TODO : être authentifié pour faire une reservation utilisation de User
#TODO : quand on clique sur reserver depuis un film on préremplis le formulaire avec lui
#TODO : mettre try except pour chaque interaction DB
#TODO movieView : si le film n'existe pas erreur releve utiliser try except DoesNotExist 

class IndexView(View):
    def get(self, request):
        prochaines_seances = Screening.objects.select_related('movie', 'cinema_room').filter(
            screening_time__gte=timezone.now()
        ).order_by('screening_time')[:3]

        return render(request, 'cinema_app/index.html', {
            'prochaines_seances': prochaines_seances,
        })


class PostLoginView(View):
    def get(self, request):
        if request.user.is_superuser or request.user.groups.filter(name__in=EMPLOYEE_GROUPS).exists():
            return redirect('employee:dashboard')
        return redirect('index')


class ReservationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = ReservationForm()
        return render(request, 'cinema_app/reservation.html', {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            hour = form.cleaned_data['hour']
            date = form.cleaned_data['date']
            heure_obj = datetime.datetime.strptime(hour, '%H:%M').time()
            screening_time = datetime.datetime.combine(date, heure_obj)

            screening, created = Screening.objects.get_or_create(
                movie=form.cleaned_data['film'],
                cinema_room=form.cleaned_data['room'],
                screening_time=screening_time,
            )

            try:
                Ticket.objects.create(
                    screening=screening,
                    person=request.user,
                    price=PRIX_BILLET,
                    seat_number=form.cleaned_data['seat_number'],
                )
            except Exception:
                messages.add_message(request, messages.ERROR, _("Ce siège est déjà réservé pour cette projection."))
                return render(request, 'cinema_app/reservation.html', {'form': form})

            messages.add_message(request, messages.SUCCESS, _("Réservation bien effectuée"))
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

            messages.add_message(request, messages.SUCCESS, _("Message bien envoyé"))
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
            messages.add_message(request, messages.SUCCESS, _("Compte créé avec succès !"))
            return redirect('index')

        return render(request, 'registration/register.html', {'form': form})


class AccountView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        tickets = request.user.tickets.all().order_by('screening__screening_time')
        return render(request, 'cinema_app/account.html', {
            'form': form,
            'tickets': tickets,
            'now': timezone.now(),
        })

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Profil mis à jour."))
            return redirect('account')

        tickets = request.user.tickets.all().order_by('screening__screening_time')
        return render(request, 'cinema_app/account.html', {
            'form': form,
            'tickets': tickets,
        })


class DeleteTicketView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, person=request.user)
        return render(request, 'cinema_app/delete_ticket_confirm.html', {'ticket': ticket})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, person=request.user)

        if ticket.screening.screening_time < timezone.now():
            messages.add_message(request, messages.ERROR, _("Impossible d'annuler un billet pour une projection passée."))
            return redirect('account')

        ticket.delete()
        messages.add_message(request, messages.SUCCESS, _("Billet annulé."))
        return redirect('account')