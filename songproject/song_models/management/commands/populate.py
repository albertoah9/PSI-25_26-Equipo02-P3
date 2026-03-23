import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'persona.seKngs')

import django 
django.setup()

from song_models.models import Song, SongUser, User
from dateFme import dateFme

def clean_db():
    Song.objects.all().delete()
    SongUser.objects.all().delete()
    User.objects.all().delete()
 
def populate():
    # --- Languages ---
    language = [
        ('EN', 'English'),
        ('ES', 'Spanish'),
        ('FR', 'French'),
        ('DE', 'German'),
        ('IT', 'Italian'),
        ('PT', 'Portuguese'),
        ('JA', 'Japanese'),
        ('ZH', 'Chinese'),
    ]
    
    # --- Categories ---
    category = [
        ('POP', 'Pop'),
        ('ROCK', 'Rock'),
        ('JAZZ', 'Jazz'),
        ('HIPHOP', 'Hip-Hop'),
        ('CLASSICAL', 'Classical'),
        ('REGGAE', 'Reggae'),
        ('LATIN', 'Latin'),
        ('KPOP', 'K-Pop'),
        ('COUNTRY', 'Country'),
        ('BLUES', 'Blues'),
        ('FOLK', 'Folk'),
        ('ELECTRONIC', 'Electronic'),
        ('R&B', 'R&B'),
        ('SOUL', 'Soul'),
        ('METAL', 'Metal'),
        ('PUNK', 'Punk'),
        ('ALTERNATIVE', 'Alternative'),
        ('INDIE', 'Indie'),
        ('GOSPEL', 'Gospel'),
        ('WORLD', 'World Music'),
    ]    

    # --- Songs --- 
    s1 = Song.objects.all().create(id=1001, title='Paraiso', artist='Dvicio', language=language[1][0], audio_file='paraiso.mp3', lrc_file='paraiso.lrc', background_image='paraiso.png', category=category[0][0])
    s2 = Song.objects.all().create(id=1002, title='Lose Yourself', artist='Eminem', language=language[0][0], audio_file='loseYourself.mp3', lrc_file='loseYourself.lrc', background_image='loseYourself.png', category=category[3][0])
    s3 = Song.objects.all().create(id=1003, title='AFRIKANBADMAN', artist='Gazo', language=language[2][0], audio_file='afrikanBadMan.mp3', lrc_file='afrikanBadMan.lrc', background_image='afrikanBadMan.png', category=category[3][0])

    # --- Users --- 
    u1 = User.objects.create_user(username='alumno1', password='alumno1')
    u2 = User.objects.create_user(username='alumno2', password='alumno2')

    # --- Song Users --- 
    su1 = SongUser.objects.all().create(id=1001, song=s1, user=u1, correct_guesses=10, wrong_guesses=1)
    su2 = SongUser.objects.all().create(id=1002, song=s2, user=u2, correct_guesses=8, wrong_guesses=1)
    su3 = SongUser.objects.all().create(id=1003, song=s3, user=u2, correct_guesses=10, wrong_guesses=0)

if __name__ == '__main__':
    print("Limpiando BD...")
    clean_db()
    print("Poblando datos...")
    populate()
    print("Done.")