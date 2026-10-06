from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from .models import Genre, Movie, CinemaRoom, Screening, Ticket, ContactMessage

#TODO : personnaliser l'affichage

admin.site.register(CinemaRoom)
admin.site.register(Screening)
admin.site.register(Ticket)
admin.site.register(ContactMessage)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "view_movies_link")
    ordering = ['name',]
    readonly_fields = ("movies_list",)

    def movies_list(self, obj):
        if not obj.pk:
            return "-"

        movies = obj.movies.all()
        if not movies:
            movie_links = "Aucun film associé"
        else:
            movie_links = format_html_join(
                mark_safe("<br>"),
                '<a href="{}">{}</a>',
                (
                    (
                        reverse("admin:cinema_app_movie_change", args=[m.pk]),
                        m.title,
                    )
                    for m in movies
                )
            )

        # Lien pour ajouter un film avec le genre pré-rempli
        add_url = (
            reverse("admin:cinema_app_movie_add")
            + f"?genre={obj.pk}"
        )
        add_link = format_html(
            '<br><br><a class="addlink" href="{}">Ajouter un film</a>',
            add_url
        )

        return format_html("{}{}", movie_links, add_link)

    movies_list.short_description = "Films associés"

    def view_movies_link(self, obj):
        url = (
            reverse("admin:cinema_app_movie_changelist")
            + f"?genre__id__exact={obj.id}"
        )
        return format_html('<a href="{}">Voir les films</a>', url)

    view_movies_link.short_description = "Films associés"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["movie_poster_image", "title", "genre", "release_date"]
    list_filter = ["genre", "release_date"]
    ordering = ["title"]
    readonly_fields = ["movie_poster_preview"]
    search_fields = ["title"]

    def movie_poster_image(self, obj):
        if obj.movie_poster:
            return format_html(
                '<span style="display:flex; align-items:center;">'
                '<img src="{}" style="max-width:32px; margin-right:6px;" />'
                '{}'
                '</span>',
                obj.movie_poster.url,
                obj.title,
            )
        return obj.title
    movie_poster_image.short_description = "Nom"
    movie_poster_image.admin_order_field = 'title'

    def movie_poster_preview(self, obj):
        if obj.movie_poster:
            return format_html('<img src="{}" style="max-width:200px" />', obj.movie_poster.url)
        return ""
    movie_poster_preview.short_description = "Prévisualisation"

    def get_readonly_fields(self, request, obj=None):
        # Permet de ne pas afficher "Image Preview" lors de l'ajout
        if obj:  # si c'est lors de la modification
            return self.readonly_fields
        return []