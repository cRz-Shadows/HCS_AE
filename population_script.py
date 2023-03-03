import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HCS_AE.settings')

import django

django.setup()

from HCS_AE.models import Movies


def add_data(data):
    d, created = Movies.objects.get_or_create(movieName=data)
    print("- Data: {0}, Created: {1}".format(str(d), str(created)))
    return d


def populate():
    # data is a list of lists
    data = ['Avatar', 'American Psycho', 'The Godfather', 'Superbad', 'Iron Man', 'The Northman']
    for movie in data:
        add_data(movie)


if __name__ == "__main__":
    populate()
