from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Post, Comment
from .validators import (
    validate_adult,
    validate_password_complexity,
    validate_title_words,
)
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "phone", "birth_date"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "validators": [validate_password_complexity],
            },
            "birth_date": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["token"] = instance.auth_token.key
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "text", "author", "created_at", "updated_at"]
        read_only_fields = ["author"]
        extra_kwargs = {
            "title": {"max_length": 200, "validators": [validate_title_words]}
        }

    def validate(self, data):
        user = self.context["request"].user
        try:
            validate_adult(user.birth_date)
        except ValidationError as e:
            raise serializers.ValidationError({"birth_date": str(e)})
        return data

    def validate_title(self, data):
        if "title" in data:
            validate_title_words(data["title"])
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author"]
