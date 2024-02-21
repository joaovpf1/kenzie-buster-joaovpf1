from django.shortcuts import render
from movies.models import Movie
from rest_framework.views import APIView
from rest_framework.request import Request
from movies.pagination import CustomPagination
from movies.permissions import IsAdminOrReadOnly
from movies.serializers import MovieSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)


# Create your views here.
class MovieView(APIView, CustomPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request):
        by_trait = request.query_params.get("trait", None)
        if by_trait:
            movies = Movie.objects.filter(traits__title__icontains=by_trait)
        else:
            movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        all_movies = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(all_movies.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(found_movie)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        found_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
