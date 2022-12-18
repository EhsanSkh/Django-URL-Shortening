from django.contrib.auth import get_user_model
from rest_framework import serializers
from shortener.models import URL

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        min_length=5,
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "confirm_password"]

    def create(self, validated_data):
        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class URLShortenerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = URL
        fields = ["pk", "main_url", "short_url", "user", "created"]
        read_only_fields = ["pk", "short_url", "user", "created"]
