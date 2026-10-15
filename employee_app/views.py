from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import EmployeeRequiredMixin
from .forms import MovieForm
from cinema_app.models import Movie

#TODO : mettre dans toutes les classes de vues le mixin EmployeeRequiredMixin pour restreindre l'accès aux employés
class DashboardView(EmployeeRequiredMixin, View):
    def get(self, request):
        return render(request, 'employee_app/dashboard.html')


class MovieListView(EmployeeRequiredMixin, ListView):
    queryset = Movie.objects.select_related('genre')
    template_name = 'movie/movies.html'
    context_object_name = 'movies'
    paginate_by = 10
        
    def has_permission(self):
        user = self.request.user
        return any(user.has_perm(f'cinema_app.{action}_movie') 
                   for action in ('view', 'add', 'change', 'delete'))



class MovieCreateView(EmployeeRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'cinema_app.add_movie'
    model = Movie
    form_class = MovieForm
    template_name = 'movie/movie_form.html'
    success_url = reverse_lazy('employee:movies')
    success_message = "Le film « %(title)s » a été ajouté."


class MovieUpdateView(EmployeeRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'cinema_app.change_movie'
    model = Movie
    form_class = MovieForm
    template_name = 'movie/movie_form.html'
    success_url = reverse_lazy('employee:movies')
    success_message = "Le film « %(title)s » a été Modifié."


class MovieDeleteView(EmployeeRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'cinema_app.delete_movie'
    model = Movie
    template_name = 'movie/movie_delete.html'
    success_url = reverse_lazy('employee:movies')

    def get_success_message(self, cleaned_data):
        return f"Le film « {self.object.title} » a été supprimé."