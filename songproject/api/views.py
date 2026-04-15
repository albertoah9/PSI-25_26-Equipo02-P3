from django.shortcuts import render
from rest_framework import viewsets
from song_models.models import Song, SongUser
from .serializers import SongSerializer, SongUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import SongPagination
from random import choice
from rest_framework.decorators import action
from rest_framework.response import Response

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all().order_by('id')
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
        if n is None:
            return Response(
                {'detail': 'Falta parametro n'},
                status=400 
            )

        try:
            n = int(n)
        except ValueError:
            return Response(
                {'detail': 'n tiene que ser int'},
                status=400 
            )
            
        songs=Song.objects.order_by('-number_times_played')[:n]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        title = request.query_params.get('title') 
        if title is None:
            return Response(
                {'detail': 'Parametro title invalido'},
                status=400 
            )
            
        songs = Song.objects.filter(title__icontains=title)
        if not songs.exists():
            return Response(
                {'detail': 'La cancion no existe'},
                status=404
            )
            
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)
    
class SongUserViewSet(viewsets.ModelViewSet):
    queryset = SongUser.objects.all()
    serializer_class = SongUserSerializer
    
    def get_queryset(self):
        return SongUser.objects.filter(user=self.request.user).order_by('id')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
