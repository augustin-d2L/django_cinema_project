from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from .models import Genre, Movie, CinemaRoom, Screening, Ticket, ContactMessage

admin.site.site_header = "CinéApp — Administration"
admin.site.site_title = "CinéApp"
admin.site.index_title = "Gestion du cinéma"

@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ("name", "view_movies_link")
    ordering = ['name',]
    readonly_fields = ("movies_list",)
    search_fields = ["name"]

    @admin.display(description="Films associés")
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

    @admin.display(description="Films")
    def view_movies_link(self, obj):
        url = (
            reverse("admin:cinema_app_movie_changelist")
            + f"?genre__id__exact={obj.id}"
        )
        return format_html('<a href="{}">Voir les films</a>', url)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ["movie_poster_image", "genre", "release_date"]
    list_filter = ["genre", "release_date"]
    list_select_related = ["genre"]
    ordering = ["title"]
    readonly_fields = ["movie_poster_preview"]
    search_fields = ["title"]

    @admin.display(description="Nom", ordering="title")
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

    @admin.display(description="Prévisualisation")
    def movie_poster_preview(self, obj):
        if obj.movie_poster:
            return format_html('<img src="{}" style="max-width:200px" />', obj.movie_poster.url)
        return ""

    def get_readonly_fields(self, request, obj=None):
        # Permet de ne pas afficher "Image Preview" lors de l'ajout
        if obj:  # si c'est lors de la modification
            return self.readonly_fields
        return []


@admin.register(CinemaRoom)
class CinemaRoomAdmin(admin.ModelAdmin):
    list_display = ["number", "capacity"]
    ordering = ["number"]


@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ["movie", "cinema_room", "screening_time"]
    list_filter = ["cinema_room", "movie"]
    search_fields = ["movie__title"]
    date_hierarchy = "screening_time"
    list_select_related = ["movie", "cinema_room"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["screening", "seat_number", "person", "status", "price"]
    list_filter = ["status", "screening__cinema_room"]
    search_fields = ["person__username", "seat_number", "screening__movie__title"]
    list_select_related = ["screening__movie", "screening__cinema_room", "person"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["email_address", "message_content"]
    search_fields = ["email_address", "message_content"]
    readonly_fields = ["email_address", "message_content"]

    def has_add_permission(self, request):
        return False