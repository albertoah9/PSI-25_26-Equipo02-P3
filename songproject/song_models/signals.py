from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Song, SongUser

@receiver(post_save, sender=SongUser)
def increment_number_times_played(sender, instance, created, **kwargs):
    if created:
        song = instance.song
        song.number_times_played += 1
        song.save()