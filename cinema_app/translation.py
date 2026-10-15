from modeltranslation.translator import register, TranslationOptions
from .models import Genre, Movie


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'description')