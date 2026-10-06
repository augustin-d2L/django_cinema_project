from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver

from .models import Movie

@receiver(post_delete, sender=Movie)
def movie_post_delete(sender, instance, **kwargs):
    # Permet de supprimer l'image du film sur le disque.
    instance.movie_poster.delete(False)  # Passez False pour ne pas enregistrer le modèle.

@receiver(pre_save, sender=Movie)
def movie_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_movie_poster = sender.objects.get(pk=instance.pk).movie_poster
            if old_movie_poster != instance.movie_poster:
                # Permet de supprimer l'ancienne image du film sur le disque si modifiée.
                old_movie_poster.delete(False)  # Passez False pour ne pas enregistrer le modèle.
        except Movie.DoesNotExist:
            pass