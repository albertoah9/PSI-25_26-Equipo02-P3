from rest_framework import serializers
from song_models.models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
