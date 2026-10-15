document.addEventListener('DOMContentLoaded', () => {
    const posterInput = document.getElementById('id_movie_poster');
    const posterPreview = document.getElementById('poster-preview');
    const posterPlaceholder = document.getElementById('poster-placeholder');

    if (!posterInput) return;

    posterInput.addEventListener('change', () => {
        const file = posterInput.files[0];
        if (!file) return;

        posterPreview.src = URL.createObjectURL(file);
        posterPreview.classList.remove('hidden');
        posterPlaceholder.classList.add('hidden');
    });
});