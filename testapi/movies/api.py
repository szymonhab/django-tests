from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, mixins, status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from movies import serializers, services, OmdbApiException
from movies.models import Comment, Movie


class StandardResultsSetPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MovieViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Movie.objects.order_by('pk')
    serializer_class = serializers.MovieSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('title', 'year', 'imdb_id')
    pagination_class = StandardResultsSetPagination

    def fetch_movies(self, request, *args, **kwargs):
        title = request.POST.get('title')
        if not title:
            return Response(
                'The url parameter "title" is missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            data = services.fetch_movie_omdapi(title)
        except OmdbApiException as exception:
            return Response(
                str(exception), status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class CommentViewSet(generics.ListCreateAPIView):

    queryset = Comment.objects.order_by('pk')
    serializer_class = serializers.CommentSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ('movie',)
    filter_backends = (DjangoFilterBackend,)



