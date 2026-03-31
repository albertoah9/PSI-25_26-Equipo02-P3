from rest_framework.pagination import PageNumberPagination

class SongPagination(PageNumberPagination):
    page_size = 3
