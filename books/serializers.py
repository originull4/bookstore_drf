from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import Author, Genre, Book


class AuthorSerializer(ModelSerializer):
    author_detail_url = HyperlinkedIdentityField(view_name='author-detail', lookup_field='slug', read_only=True)
    author_books_url = HyperlinkedIdentityField(view_name='author-books', lookup_field='slug', read_only=True)

    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {'slug': {'read_only': True}, }


class GenreSerializer(ModelSerializer):
    genre_detail_url = HyperlinkedIdentityField(view_name='genre-detail', lookup_field='slug', read_only=True)
    genre_books_url = HyperlinkedIdentityField(view_name='genre-books', lookup_field='slug', read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'
        extra_kwargs = {'slug': {'read_only': True}, }


class BookSerializer(ModelSerializer):
    book_detail_url = HyperlinkedIdentityField(view_name='book-detail', lookup_field='slug', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {'slug': {'read_only': True}, }

    # def get_pdf(self):
    #     user = self.context['request'].user

