import json
from accounts.models import Account
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Author, Book, Genre


superuser_data = {'username': 'admin_user', 'password': 'admin_user_pass'}
staff_user_data = {'username': 'staff1', 'password': 'staff1pass'}

author_data = {'name': 'author name', 'description': 'some description about author'}
author_data2 = {'name': 'other author', 'description': 'some description about author'}

genre_data = {'title': 'genre title', 'description': 'some description about genre'}
genre_data2 = {'title': 'other genre', 'description': 'some description about genre'}

book_data = {'title': 'book title', 'description': 'some description about book'}


class BookViewSetTestCase(APITestCase):
    
    def setUp(self) -> None:
        # create a superuser        
        self.superuser = Account.objects.create_superuser(**superuser_data)
        
        # create a staff user        
        self.staff_user = Account.objects.create_user(**staff_user_data)
        
        # get created superuser tokens with rest_framework_simplejwt TokenObtainPair View
        admin_auth = self.client.post(reverse('token_obtain_pair'), superuser_data).data
        # Authorization with access token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_auth['access'])

        self.book = Book.objects.create(**book_data)



class AuthorViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        # create a superuser        
        self.superuser = Account.objects.create_superuser(**superuser_data)
        
        # create a staff user        
        self.staff_user = Account.objects.create_user(**staff_user_data)
        
        # get created superuser tokens with rest_framework_simplejwt TokenObtainPair View
        admin_auth = self.client.post(reverse('token_obtain_pair'), superuser_data).data
        # Authorization with access token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_auth['access'])

        # create an author        
        self.author = Author.objects.create(**author_data)


    def test_authors_list(self):
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_create(self):
        url = reverse('author-list')
        response = self.client.post(url, author_data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_author_create_by_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('author-list')
        response = self.client.post(url, author_data2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_create_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('author-list')
        response = self.client.post(url, author_data2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_detail(self):
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], self.author.name)

    def test_author_update(self):
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.put(url, author_data2)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], author_data2['name'])

    def test_author_update_by_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.put(url, author_data2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_update_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.put(url, author_data2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_delete(self):
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_author_delete_by_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_delete_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('author-detail', kwargs={'slug': self.author.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GenreViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        # create a superuser        
        self.superuser = Account.objects.create_superuser(**superuser_data)
        
        # create a staff user        
        self.staff_user = Account.objects.create_user(**staff_user_data)
        
        # get created superuser tokens with rest_framework_simplejwt TokenObtainPair View
        admin_auth = self.client.post(reverse('token_obtain_pair'), superuser_data).data
        # Authorization with access token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_auth['access'])

        # create an author        
        self.genre = Genre.objects.create(**genre_data)


    def test_genres_list(self):
        url = reverse('genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_create(self):
        url = reverse('genre-list')
        response = self.client.post(url, genre_data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_create_by_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('genre-list')
        response = self.client.post(url, genre_data2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_genre_create_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('genre-list')
        response = self.client.post(url, genre_data2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_genre_detail(self):
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.get(url)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], self.genre.title)

    def test_genre_update(self):
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.put(url, genre_data2)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], genre_data2['title'])

    def test_genre_update_by_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.put(url, genre_data2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_genre_update_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.put(url, genre_data2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_genre_delete(self):
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_genre_delete_by_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_genre_delete_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('genre-detail', kwargs={'slug': self.genre.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
