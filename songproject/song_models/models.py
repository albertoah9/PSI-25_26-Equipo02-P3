from django.db import models
from  django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.artist}"

class SongUser(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)
    correct_guesses = models.IntegerField(default=0)
    wrong_guesses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.song} - {self.user}"

    