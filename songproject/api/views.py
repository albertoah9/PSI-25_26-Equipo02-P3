from django.shortcuts import render
from rest_framework import viewsets
from song_models.models import Song, SongUser
from .serializers import SongSerializer, SongUserSerializer
from rest_framework.permissions import AllowAny
from .pagination import SongPagination
from random import choice
from rest_framework.decorators import action
from rest_framework.response import Response

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all().order_by('id') # aqui he metido el order by porque si no el test da un warning de paginacion
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
        # si falta la n hay que devolver 400 bad request (esto lo he metido nuevo)
        if n is None:
            return Response(
                {'detail': 'Falta parametro n'},
                status=400 
            )

        try:
            n = int(n)
        except ValueError:
            #aqui he quitado lo de n = 3 porque los test fallan
            return Response(
                {'detail': 'n tiene que ser int'},
                status=400 
            )
            
        songs=Song.objects.order_by('-number_times_played')[:n]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        # antes estaba con ('title', '') con esa opcion si no se mandaba title se ponia como vacio y falla el test
        title = request.query_params.get('title') 
        # si no hay titulo se devuelve 400
        if title is None:
            return Response(
                {'detail': 'Parametro title invalido'},
                status=400 
            )
        songs = Song.objects.filter(title__icontains=title)
        # si la cancion no existe se devuelve 400
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
    
    # se obtienen solo los datos del usuario que hace la request y no de otros
    def get_queryset(self):
        return SongUser.objects.filter(user=self.request.user).order_by('id')
    
    # Cuando haces post guarda solo el usuario que hace el post, de manera que no hay que meter el user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

