from rest_framework import serializers

from movies.models import Comment, Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class ExternalMovieSerializer(serializers.Serializer):

    Title = serializers.CharField(max_length=255, source='title')
    Year = serializers.IntegerField(source='year')
    Rated = serializers.CharField(max_length=63, source='rated')
    Released = serializers.DateField(
        source='released', input_formats=('%d %b %Y',)
    )
    Runtime = serializers.CharField(max_length=63, source='runtime')
    Genre = serializers.CharField(max_length=1023, source='genre')
    Director = serializers.CharField(max_length=255, source='director')
    Writer = serializers.CharField(max_length=255, source='writer')
    Actors = serializers.CharField(max_length=255, source='actors')
    Plot = serializers.CharField(source='plot')
    Language = serializers.CharField(max_length=1023, source='language')
    Country = serializers.CharField(max_length=1023, source='country')
    Awards = serializers.CharField(max_length=255, source='awards')
    Poster = serializers.CharField(max_length=255, source='poster')
    Ratings = serializers.JSONField(source='ratings')
    Metascore = serializers.IntegerField(source='metascore')
    imdbRating = serializers.CharField(max_length=63, source='imdb_rating')
    imdbVotes = serializers.IntegerField(source='imdb_votes')
    imdbID = serializers.CharField(max_length=63, source='imdb_id')
    Type = serializers.CharField(max_length=63, source='type')
    DVD = serializers.DateField(source='dvd', input_formats=('%d %b %Y',))
    BoxOffice = serializers.CharField(max_length=63, source='box_office')
    Production = serializers.CharField(max_length=255, source='production')
    Website = serializers.CharField(max_length=255, source='website')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
