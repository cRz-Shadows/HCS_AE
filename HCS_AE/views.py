from HCS_AE.models import Movies
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
import tmdb
import requests
import random

API_KEY = 'a2b67da805cffb9ba951a0f56da1e603'

def movie_details(request):
    movie_titles = [movie.movieName for movie in Movies.objects.all()[:5]]
    if movie_titles:
        data = []
        for movie_title in movie_titles:
            movie_data = get_movie_details(movie_title)
            movies = get_movies_in_genre(movie_data['genre_id'], movie_title)
            movies = [{'title': movie_data['title'], 'poster_url': movie_data['poster_url'], 'correct_answer': True}] + movies
            random.shuffle(movies)
            data = data + [movies]
        if len(data) == 5:
            data = {'q1': data[0], 'q2': data[1], 'q3': data[2], 'q4': data[3], 'q5': data[4]}
            return JsonResponse(data)
        elif 5 > len(data) > 0:
            return JsonResponse(data)
    else:
        return HttpResponse('No movie title provided.')


def get_movie_details(movie_title):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}'
    response = requests.get(url)
    movie_data = response.json().get('results')[0]
    title = movie_data['title']
    genre_id = random.choice(movie_data['genre_ids'])
    poster_path = movie_data['poster_path']
    poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
    return {'title': title, 'poster_url': poster_url, 'genre_id': genre_id}


def get_movies_in_genre(genre, movie_title):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre}'
    response = requests.get(url)
    movies_data = response.json()['results']
    random.shuffle(movies_data)
    movies = []
    for movie_data in movies_data:
        title = movie_data['title']
        poster_path = movie_data['poster_path']
        poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
        movies.append({'title': title, 'poster_url': poster_url, 'correct_answer': False})
    _movies = [movie for movie in movies[:8] if movie['title'] != movie_title]
    if len(_movies) == 8:
        return _movies
    else:
        return [movie for movie in movies[:9] if movie['title'] != movie_title]


def movies_in_genre(request, genre):
    movies = tmdb.get_movies_in_genre(genre)
    return JsonResponse({'movies': movies})
