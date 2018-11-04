import json

import pytest
import responses
from django.conf import settings

from movies.models import Comment, Movie
from movies.serializers import MovieSerializer


pytestmark = pytest.mark.django_db


@pytest.fixture
def external_movie_schema():
    return {
        'Title': 'TestMovie',
        'Year': '2018',
        'Rated': 'PG-13',
        'Released': '01 Jun 2018',
        'Runtime': '65 min',
        'Genre': 'Action, Sci-Fi',
        'Director': 'Kowalski',
        'Writer': 'John Smith',
        'Actors': 'Joseph Marshall, Ian King',
        'Plot': 'Some twisted plot',
        'Language': 'English, French',
        'Country': 'USA, UK',
        'Awards': 'Won 2 Oscars.',
        'Poster': 'some-poster-path',
        'Ratings': [
            {'Source': 'Internet Movie Database', 'Value': '5.8/10'},
            {'Source': 'Rotten Tomatoes', 'Value': '66%'}
        ],
        'Metascore': '65',
        'imdbRating': '5.9',
        'imdbVotes': '54,951',
        'imdbID': 'tt2357596',
        'Type': 'movie',
        'DVD': '11 Aug 2018',
        'BoxOffice': '$512,841',
        'Production': 'Some company',
        'Website': 'some-website',
        'Response': 'True'
    }


@pytest.fixture
def movie_schema():
    return {
        'title': 'TestMovie',
        'year': 2018,
        'rated': 'PG-13',
        'released': '2018-06-01',
        'runtime': '65 min',
        'genre': ['Action', 'Sci-Fi'],
        'director': 'Kowalski',
        'writer': 'John Smith',
        'actors': 'Joseph Marshall, Ian King',
        'plot': 'Some twisted plot',
        'language': ['English', 'French'],
        'country': ['USA', 'UK'],
        'awards': 'Won 2 Oscars.',
        'poster': 'some-poster-path',
        'ratings': [
            {'Source': 'Internet Movie Database', 'Value': '5.8/10'},
            {'Source': 'Rotten Tomatoes', 'Value': '66%'}
        ],
        'metascore': 65,
        'imdb_rating': '5.9',
        'imdb_votes': 54951,
        'imdb_id': 'tt2357596',
        'type': 'movie',
        'dvd': '2018-08-11',
        'box_office': '$512,841',
        'production': 'Some company',
        'website': 'some-website'
    }


@pytest.fixture
def movie(movie_schema):
    return Movie.objects.create(**movie_schema)


@pytest.fixture
def different_movie(movie_schema):
    return Movie.objects.create(**dict(movie_schema, imdb_id='different'))


@pytest.fixture
def comments(movie, different_movie):
    Comment.objects.create(text='test1', movie=movie)
    Comment.objects.create(text='test2', movie=different_movie)
    Comment.objects.create(text='test3', movie=different_movie)


@pytest.mark.usefixtures('movie')
def test_get_movies(client, movie_schema):
    response = client.get('/movies/')
    assert response.status_code == 200
    assert response.json()['results'] == [movie_schema]


@responses.activate
def test_fetch_movies(client, movie_schema, external_movie_schema):
    with responses.RequestsMock() as requests_mock:
        requests_mock.add(
            responses.GET,
            (
                f'http://www.omdbapi.com/'
                f'?apikey={settings.MOVIES_API_KEY}&t=TestMovie'
            ),
            body=json.dumps(external_movie_schema),
            status=200,
            content_type='application/json'
        )
        response = client.post('/movies/', data={'title': 'TestMovie'})
    assert response.status_code == 201
    movie_data = MovieSerializer(Movie.objects.first()).data
    assert movie_data == movie_schema
    assert response.json() == movie_schema


@responses.activate
def test_failed_fetch_movies(client, movie_schema, external_movie_schema):
    with responses.RequestsMock() as requests_mock:
        requests_mock.add(
            responses.GET,
            (
                f'http://www.omdbapi.com/'
                f'?apikey={settings.MOVIES_API_KEY}&t=TestMovie'
            ),
            body='{"Response": "False"}',
            status=200,
            content_type='application/json'
        )
        response = client.post('/movies/', data={'title': 'TestMovie'})
    assert response.status_code == 404
    assert not Movie.objects.exists()
    assert response.json() == 'Omdb Api Error.'


def test_post_comment(client, movie):
    response = client.post(
        '/comments/', data={
            'movie': movie.imdb_id,
            'text': 'test comment'
        }
    )
    comment = Comment.objects.first()
    assert comment.text == 'test comment'
    assert comment.movie == movie
    expected_response = {
        'id': comment.id, 'text': 'test comment', 'movie': 'tt2357596'
    }
    assert response.json() == expected_response


@pytest.mark.usefixtures('comments')
def test_get_comments(client):
    response = client.get('/comments/')
    comments = set(it['text'] for it in response.json()['results'])
    assert comments == {'test1', 'test2', 'test3'}


@pytest.mark.usefixtures('comments')
def test_filter_comments(client, different_movie):
    response = client.get(f'/comments/?movie={different_movie.imdb_id}')
    comments = set(it['text'] for it in response.json()['results'])
    assert comments == {'test2', 'test3'}
