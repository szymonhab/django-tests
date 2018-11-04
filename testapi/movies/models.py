from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class Movie(models.Model):

    imdb_id = models.CharField(max_length=63, primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    rated = models.CharField(max_length=63)
    released = models.DateField()
    runtime = models.CharField(max_length=63)
    genre = ArrayField(models.CharField(max_length=31, blank=True))
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    actors = models.CharField(max_length=1023)
    plot = models.TextField()
    language = ArrayField(models.CharField(max_length=31, blank=True))
    country = ArrayField(models.CharField(max_length=31, blank=True))
    awards = models.CharField(max_length=255)
    poster = models.CharField(max_length=255)
    ratings = JSONField()
    metascore = models.IntegerField()
    imdb_rating = models.CharField(max_length=63)
    imdb_votes = models.IntegerField()
    type = models.CharField(max_length=63)
    dvd = models.DateField()
    box_office = models.CharField(max_length=63)
    production = models.CharField(max_length=255)
    website = models.CharField(max_length=255)


class Comment(models.Model):

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
