import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'persona.seKngs')

import django 
django.setup()

from song_models.models import Song, SongUser
from dateFme import dateFme

def clean_db():
    Song.objects.all().delete()
    SongUser.objects.all().delete()
 
def populate():
    # --- Usuarios --- 
    s1 = Song.objects.all().create()
    
    p1 = Persona.objects.create(id=1001, nombre='Rubén', apellido='Somavilla', email='ruben.somavilla@estudiante.uam.es') 
    p2 = Persona.objects.create(id=1002, nombre='Germám', apellido = 'Tomé', email='german.tome@estudiante.uam.es') 
    p3 = Persona.objects.create(id=1003, nombre='Alejandro', apellido = 'Moya', email= 'alejandro.moya@estudiante.uam.es')
        
if __name__ == '__main__':
    print("Limpiando BD...")
    clean_db()
    print("Poblando datos...")
    populate()
    print("Done.")