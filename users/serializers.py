from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            )
        ]
    )
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="email already registered."
            )
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(default=None)
    is_employee = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True, max_length=150)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        if validated_data["is_employee"] is False:
            user = User.objects.create_user(**validated_data)
        else:
            user = User.objects.create_superuser(**validated_data)
        return user

    def update(self, instance: User, validated_data: dict):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
