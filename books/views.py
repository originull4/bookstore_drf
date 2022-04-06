from core.permissions import IsAdminOrReadOnly
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK
from .models import Author, Book, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]


    @action(detail=False)
    def author_books(self, request, slug):
        books = self.get_queryset().filter(author__slug=slug)
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=False)
    def genre_books(self, request, slug):
        books = self.get_queryset().filter(genres__slug=slug)
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)
