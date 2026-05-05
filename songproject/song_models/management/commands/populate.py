from django.core.management.base import BaseCommand
from song_models.models import Song, SongUser
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Limpiando BD...")

        # Limpiar datos
        SongUser.objects.all().delete()
        Song.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Poblando datos...")

        # --- Songs ---
        s1 = Song.objects.create(id=3, title='Super Trouper', artist='ABBA', language='EN', audio_file='ABBA - Super Trouper.mp3', lrc_file='ABBA - Super Trouper.lrc', background_image='ABBA - Super Trouper.jpg', category='POP')
        s2= Song.objects.create(title='Here In The Real World', artist='Alan Jackson', language='EN', audio_file='Alan Jackson - Here In The Real World.mp3', lrc_file='Alan Jackson - Here In The Real World.lrc', background_image='Alan Jackson - Here In The Real World.jpg', category='COUNTRY')
        s3 = Song.objects.create(title='Don\'t Forget to Remember', artist='Beegees', language='EN', audio_file='Beegees - Don\'t Forget to Remember.mp3', lrc_file='Beegees - Don\'t Forget to Remember.lrc', background_image='Beegees - Don\'t Forget to Remember.png', category='POP')

        # --- Users ---
        u1 = User.objects.create_user(username='alumno1', password='alumno1')
        u2 = User.objects.create_user(username='alumno2', password='alumno2')

        User.objects.create_superuser(username='alumnodb', password='alumnodb')

        # --- SongUser ---
        SongUser.objects.create(song=s1, user=u1, correct_guesses=10, wrong_guesses=1)
        SongUser.objects.create(song=s2, user=u2, correct_guesses=8, wrong_guesses=1)
        SongUser.objects.create(song=s3, user=u2, correct_guesses=10, wrong_guesses=0)

        self.stdout.write(self.style.SUCCESS("Base de datos poblada correctamente"))
