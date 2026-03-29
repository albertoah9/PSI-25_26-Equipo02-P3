from django.shortcuts import render
from rest_framework import viewsets
from song_models.models import Song
from .serializers import SongSerializer
from rest_framework.permissions import AllowAny
from .pagination import SongPagination
from random import choice
from rest_framework.decorators import action
from rest_framework.response import Response

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny]
    pagination_class = SongPagination
    
    @action(detail=False, methods=['get'])
    def random(self, request):
        songs = list(Song.objects.all())
        if not songs:
            return Response({'detail': 'No songs available'}, status=404)
        
        song=choice(songs)
        serializer = self.get_serializer(song)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        n=request.query_params.get('n', 3)
        try:
            n = int(n)
        except ValueError:
            n=3
            
        songs=Song.objects.order_by('-number_times_played')[:n]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        title = request.query_params.get('title', '')
        songs = Song.objects.filter(title__icontains=title)
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

