from rest_framework import serializers
from traitlets import default
from movies.models import Movie, RatingOptions
from users.models import User


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default="", allow_null=True)
    rating = serializers.ChoiceField(choices=RatingOptions, default=RatingOptions.G)
    synopsis = serializers.CharField(default="", allow_null=True)
    added_by = serializers.CharField(read_only=True, source="user.email")

    def create(self, validated_data):
        movie = Movie.objects.create(**validated_data)
        return movie
