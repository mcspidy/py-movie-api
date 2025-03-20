from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cinema.models import Movie, Genre, Director, Actor, Review


class CinemaAppTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.genre = Genre.objects.create(name='Action')
        self.director = Director.objects.create(name='John Doe')
        self.actor = Actor.objects.create(name='Jane Doe')
        self.movie = Movie.objects.create(
            title='The Matrix',
            year=1999,
            director=self.director
        )
        self.movie.genre.add(self.genre)
        self.movie.actor.add(self.actor)
        self.review = Review.objects.create(
            movie=self.movie,
            author=self.user,
            rating=5,
            content='This is a test review'
        )

    def test_movie_list_view(self):
        response = self.client.get(reverse('cinema:movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Matrix')
        self.assertTemplateUsed(response, 'cinema/movie_list.html')

    def test_movie_detail_view(self):
        response = self.client.get(reverse('cinema:movie_detail', args=[self.movie.id]))
        no_response = self.client.get(reverse('cinema:movie_detail', args=[1000]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'The Matrix')
        self.assertTemplateUsed(response, 'cinema/movie_detail.html')

    def test_movie_create_view(self):
        response = self.client.post(reverse('cinema:movie_create'), {
            'title': 'The Matrix',
            'year': 1999,
            'director': self.director.id,
            'genre': [self.genre.id],
            'actor': [self.actor.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.last().title, 'The Matrix')

    def test_movie_update_view(self):
        response = self.client.post(reverse('cinema:movie_update', args=[self.movie.id]), {
            'title': 'The Matrix Reloaded',
            'year': 2003,
            'director': self.director.id,
            'genre': [self.genre.id],
            'actor': [self.actor.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.last().title, 'The Matrix Reloaded')

    def test_movie_delete_view(self):
        response = self.client.post(reverse('cinema:movie_delete', args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.count(), 0)
