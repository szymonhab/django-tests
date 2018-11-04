from copy import deepcopy

import requests
from django.conf import settings

from movies import OmdbApiException, serializers


def fetch_movie_omdapi(title):
    api_key = settings.MOVIES_API_KEY
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
    content = requests.get(url).json()
    if not content['Response'] == 'True':
        raise OmdbApiException(content.get('Error', 'Omdb Api Error.'))
    if content.get('imdbVotes'):
        content['imdbVotes'] = content['imdbVotes'].replace(',', '')
    serializer = serializers.ExternalMovieSerializer(data=content)
    serializer.is_valid(raise_exception=True)
    data = deepcopy(serializer.validated_data)
    for field_name in ('language', 'country', 'genre'):
        data[field_name] = data[field_name].split(',')
    return data

