from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
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

    """Fetch movie from IMDB database on POST request."""

    queryset = Movie.objects.order_by('pk')
    serializer_class = serializers.MovieSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('title', 'year', 'imdb_id')
    pagination_class = StandardResultsSetPagination

    def fetch_movies(self, request, *args, **kwargs):
        title = request.data.get('title')
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

    """Show and insert movie comments."""

    queryset = Comment.objects.order_by('pk')
    serializer_class = serializers.CommentSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ('movie',)
    filter_backends = (DjangoFilterBackend,)


class TopCommentedMovieViewSet(generics.ListAPIView):

    """Get movies ordered by their comment number, date filter is required."""

    queryset = Movie.objects.all()
    serializer_class = serializers.TopCommentedMovieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        range_serializer = serializers.DateRangeSerializer(
            data=self.request.query_params
        )
        range_serializer.is_valid(raise_exception=True)
        data = range_serializer.validated_data
        date_range = (data['date_after'], data['date_before'])
        return queryset.annotate(
            total_comments=Count(
                'comments',
                filter=Q(comments__created_at__range=date_range)
            )
        ).order_by('-total_comments')[0:5]
