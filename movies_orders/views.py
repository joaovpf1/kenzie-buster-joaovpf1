from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.models import Movie
from movies_orders.serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int):
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_order=request.user, movie_order=found_movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
