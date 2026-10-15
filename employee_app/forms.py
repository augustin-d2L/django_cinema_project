from django import forms
from cinema_app.models import Movie

INPUT_CLASSES = (
    'w-full px-3 py-2.5 rounded-md bg-white/5 border border-white/10 text-white '
    'placeholder-gray-500 focus:outline-none focus:border-cinema-red focus:ring-1 focus:ring-cinema-red '
    'transition-colors'
)

FILE_CLASSES = (
    'w-full text-sm text-gray-400 '
    'file:mr-3 file:px-3 file:py-2 file:rounded-md file:border-0 '
    'file:bg-cinema-red file:text-white file:font-semibold hover:file:bg-red-700 file:cursor-pointer'
)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'release_date', 'genre', 'movie_poster']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ex. Dune : Deuxième partie'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Synopsis du film...'}),
            'duration': forms.NumberInput(attrs={'placeholder': 'Ex. 120', 'min': 1}),
            'release_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'movie_poster':
                field.widget.attrs['class'] = FILE_CLASSES
            else:
                field.widget.attrs['class'] = INPUT_CLASSES
        self.fields['genre'].empty_label = 'Choisir un genre'