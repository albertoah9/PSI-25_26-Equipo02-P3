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
        s1 = Song.objects.create(title='Paraiso', artist='Dvicio', language='ES', audio_file='paraiso.mp3', lrc_file='paraiso.lrc', background_image='paraiso.png', category='POP')
        s2 = Song.objects.create(title='Lose Yourself', artist='Eminem', language='EN', audio_file='loseYourself.mp3', lrc_file='loseYourself.lrc', background_image='loseYourself.png', category='HIPHOP')
        s3 = Song.objects.create(title='AFRIKANBADMAN', artist='Gazo', language='FR', audio_file='afrikanBadMan.mp3', lrc_file='afrikanBadMan.lrc', background_image='afrikanBadMan.png', category='HIPHOP')
        s4= Song.objects.create(title='Here in the real world', artist='Alan Jackson', language='EN', audio_file='here_in_the_real_world.mp3', lrc_file='here_in_the_real_world.lrc', background_image='here_in_the_real_world.png', category='COUNTRY')

        # --- Users ---
        u1 = User.objects.create_user(username='alumno1', password='alumno1')
        u2 = User.objects.create_user(username='alumno2', password='alumno2')

        User.objects.create_superuser(username='alumnodb', password='alumnodb')

        # --- SongUser ---
        SongUser.objects.create(song=s1, user=u1, correct_guesses=10, wrong_guesses=1)
        SongUser.objects.create(song=s2, user=u2, correct_guesses=8, wrong_guesses=1)
        SongUser.objects.create(song=s3, user=u2, correct_guesses=10, wrong_guesses=0)

        self.stdout.write(self.style.SUCCESS("Base de datos poblada correctamente"))